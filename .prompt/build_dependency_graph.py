#!/usr/bin/env python3
"""
Dependency Graph Builder for DotPrompt Workspace

Scans repository to extract:
- File metadata (type, size, lines)
- Imports and exports
- Class definitions and inheritance
- Function/method definitions
- Type definitions and interfaces
- Identifier references
- Cross-file relationships

Outputs to: .prompt/dependency-graph.json
"""

import os
import re
import json
import ast
from pathlib import Path
from typing import Dict, List, Set, Any, Optional
from collections import defaultdict
import hashlib


class DependencyGraphBuilder:
    def __init__(self, root_dir: str):
        self.root_dir = Path(root_dir).resolve()
        self.graph = {
            "metadata": {
                "version": "1.0.0",
                "generated_at": None,
                "root_directory": str(self.root_dir),
                "total_files": 0,
                "file_types": {}
            },
            "files": {},
            "relationships": {
                "imports": [],
                "exports": [],
                "inheritance": [],
                "references": []
            },
            "modules": {}
        }

        # Directories to skip
        self.skip_dirs = {
            'node_modules', '.git', 'dist', 'build', 'coverage',
            '__pycache__', '.next', '.cache', 'public', 'static',
            '.vscode', '.idea', 'tmp', 'temp', '.turbo'
        }

        # File extensions to process
        self.file_patterns = {
            'typescript': {'.ts', '.tsx'},
            'javascript': {'.js', '.jsx', '.mjs', '.cjs'},
            'python': {'.py'},
            'csharp': {'.cs'},
            'go': {'.go'},
            'sql': {'.sql'},
            'yaml': {'.yml', '.yaml'},
            'json': {'.json'},
            'html': {'.html', '.htm'},
            'css': {'.css', '.scss', '.sass', '.less'},
            'markdown': {'.md'},
            'xml': {'.xml'},
            'shell': {'.sh', '.bash'},
        }

    def build_graph(self):
        """Main entry point to build the dependency graph"""
        print("🔍 Scanning repository...")

        # Scan all files
        for file_path in self._walk_files():
            self._process_file(file_path)

        # Post-processing: resolve relationships
        self._resolve_relationships()

        # Update metadata
        from datetime import datetime
        self.graph["metadata"]["generated_at"] = datetime.utcnow().isoformat() + "Z"
        self.graph["metadata"]["total_files"] = len(self.graph["files"])

        print(f"\n✅ Processed {len(self.graph['files'])} files")
        print(f"📊 File type distribution:")
        for file_type, count in sorted(self.graph["metadata"]["file_types"].items(), key=lambda x: x[1], reverse=True):
            print(f"   {file_type}: {count}")

        return self.graph

    def _walk_files(self):
        """Walk directory tree and yield file paths"""
        for root, dirs, files in os.walk(self.root_dir):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if d not in self.skip_dirs]

            for filename in files:
                file_path = Path(root) / filename
                ext = file_path.suffix.lower()

                # Check if we should process this file
                if any(ext in exts for exts in self.file_patterns.values()):
                    yield file_path

    def _process_file(self, file_path: Path):
        """Process a single file and extract metadata"""
        try:
            rel_path = str(file_path.relative_to(self.root_dir))
            ext = file_path.suffix.lower()

            # Get file type
            file_type = self._get_file_type(ext)

            # Update file type count
            self.graph["metadata"]["file_types"][file_type] = \
                self.graph["metadata"]["file_types"].get(file_type, 0) + 1

            # Read file content
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except (UnicodeDecodeError, PermissionError):
                # Skip binary or inaccessible files
                return

            # Count lines
            lines = content.count('\n') + 1

            # Initialize file entry
            file_info = {
                "path": rel_path,
                "type": file_type,
                "extension": ext,
                "size_bytes": file_path.stat().st_size,
                "lines": lines,
                "imports": [],
                "exports": [],
                "classes": [],
                "functions": [],
                "interfaces": [],
                "types": [],
                "constants": [],
                "dependencies": [],
                "dependents": []
            }

            # Parse based on file type
            if file_type in ('typescript', 'javascript'):
                self._parse_typescript_javascript(content, file_info)
            elif file_type == 'python':
                self._parse_python(content, file_info)
            elif file_type == 'json' and 'package.json' in rel_path:
                self._parse_package_json(content, file_info)

            self.graph["files"][rel_path] = file_info

        except Exception as e:
            print(f"⚠️  Error processing {file_path}: {e}")

    def _get_file_type(self, ext: str) -> str:
        """Map file extension to file type"""
        for file_type, exts in self.file_patterns.items():
            if ext in exts:
                return file_type
        return 'other'

    def _parse_typescript_javascript(self, content: str, file_info: Dict):
        """Parse TypeScript/JavaScript files"""

        # Extract imports
        # import x from 'module'
        # import { x, y } from 'module'
        # import * as x from 'module'
        # import type { x } from 'module'
        # const x = require('module')
        import_patterns = [
            r"import\s+(?:type\s+)?(?:\{[^}]+\}|\*\s+as\s+\w+|\w+)\s+from\s+['\"]([^'\"]+)['\"]",
            r"import\s+['\"]([^'\"]+)['\"]",
            r"require\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
            r"import\s*\(\s*['\"]([^'\"]+)['\"]\s*\)",
        ]

        for pattern in import_patterns:
            for match in re.finditer(pattern, content):
                module = match.group(1)
                if module and module not in file_info["imports"]:
                    file_info["imports"].append(module)
                    file_info["dependencies"].append(module)

        # Extract exports
        # export class X
        # export function X
        # export const X
        # export default X
        # export { X, Y }
        # export * from 'module'
        export_patterns = [
            r"export\s+(?:default\s+)?class\s+(\w+)",
            r"export\s+(?:default\s+)?function\s+(\w+)",
            r"export\s+(?:default\s+)?const\s+(\w+)",
            r"export\s+(?:default\s+)?let\s+(\w+)",
            r"export\s+(?:default\s+)?var\s+(\w+)",
            r"export\s+(?:default\s+)?interface\s+(\w+)",
            r"export\s+(?:default\s+)?type\s+(\w+)",
            r"export\s+(?:default\s+)?enum\s+(\w+)",
            r"export\s*\{([^}]+)\}",
        ]

        for pattern in export_patterns:
            for match in re.finditer(pattern, content):
                exported = match.group(1).strip()
                if ',' in exported:
                    # Handle export { X, Y }
                    exports = [e.strip().split(' as ')[0] for e in exported.split(',')]
                    file_info["exports"].extend(exports)
                else:
                    file_info["exports"].append(exported)

        # Extract class definitions
        # class X extends Y implements Z
        class_pattern = r"(?:export\s+)?(?:abstract\s+)?class\s+(\w+)(?:\s+extends\s+(\w+))?(?:\s+implements\s+([\w,\s]+))?"
        for match in re.finditer(class_pattern, content):
            class_name = match.group(1)
            extends = match.group(2)
            implements = match.group(3)

            class_info = {
                "name": class_name,
                "extends": extends,
                "implements": [i.strip() for i in implements.split(',')] if implements else []
            }
            file_info["classes"].append(class_info)

            # Track inheritance
            if extends:
                self.graph["relationships"]["inheritance"].append({
                    "file": file_info["path"],
                    "class": class_name,
                    "extends": extends
                })

        # Extract function definitions
        # function X() {}
        # const X = () => {}
        # async function X() {}
        function_patterns = [
            r"(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(",
            r"(?:export\s+)?const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>",
            r"(?:export\s+)?const\s+(\w+)\s*=\s*function",
        ]

        for pattern in function_patterns:
            for match in re.finditer(pattern, content):
                func_name = match.group(1)
                if func_name not in file_info["functions"]:
                    file_info["functions"].append(func_name)

        # Extract interface definitions
        # interface X extends Y
        interface_pattern = r"(?:export\s+)?interface\s+(\w+)(?:\s+extends\s+([\w,\s]+))?"
        for match in re.finditer(interface_pattern, content):
            interface_name = match.group(1)
            extends = match.group(2)

            interface_info = {
                "name": interface_name,
                "extends": [e.strip() for e in extends.split(',')] if extends else []
            }
            file_info["interfaces"].append(interface_info)

        # Extract type definitions
        # type X = ...
        type_pattern = r"(?:export\s+)?type\s+(\w+)\s*="
        for match in re.finditer(type_pattern, content):
            type_name = match.group(1)
            file_info["types"].append(type_name)

        # Extract enum definitions
        # enum X {}
        enum_pattern = r"(?:export\s+)?enum\s+(\w+)"
        for match in re.finditer(enum_pattern, content):
            enum_name = match.group(1)
            file_info["constants"].append(enum_name)

    def _parse_python(self, content: str, file_info: Dict):
        """Parse Python files"""
        try:
            tree = ast.parse(content)

            # Extract imports
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        module = alias.name
                        if module not in file_info["imports"]:
                            file_info["imports"].append(module)
                            file_info["dependencies"].append(module)

                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        module = node.module
                        if module not in file_info["imports"]:
                            file_info["imports"].append(module)
                            file_info["dependencies"].append(module)

                # Extract class definitions
                elif isinstance(node, ast.ClassDef):
                    bases = [self._get_name(base) for base in node.bases]
                    class_info = {
                        "name": node.name,
                        "extends": bases[0] if bases else None,
                        "implements": bases[1:] if len(bases) > 1 else []
                    }
                    file_info["classes"].append(class_info)

                    # Track inheritance
                    if bases:
                        for base in bases:
                            self.graph["relationships"]["inheritance"].append({
                                "file": file_info["path"],
                                "class": node.name,
                                "extends": base
                            })

                # Extract function definitions (top-level only)
                elif isinstance(node, ast.FunctionDef) and isinstance(node, ast.Module):
                    file_info["functions"].append(node.name)

            # Find top-level functions
            for node in tree.body:
                if isinstance(node, ast.FunctionDef):
                    file_info["functions"].append(node.name)

        except SyntaxError as e:
            print(f"⚠️  Syntax error in Python file {file_info['path']}: {e}")

    def _get_name(self, node):
        """Get name from AST node"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        return str(node)

    def _parse_package_json(self, content: str, file_info: Dict):
        """Parse package.json to extract dependencies"""
        try:
            data = json.loads(content)

            # Extract all dependency types
            for dep_type in ['dependencies', 'devDependencies', 'peerDependencies', 'optionalDependencies']:
                if dep_type in data:
                    for package_name in data[dep_type].keys():
                        if package_name not in file_info["dependencies"]:
                            file_info["dependencies"].append(package_name)
        except json.JSONDecodeError:
            pass

    def _resolve_relationships(self):
        """Resolve file-to-file relationships"""
        print("\n🔗 Resolving relationships...")

        # Build a mapping of module names to file paths
        module_map = {}

        for file_path, file_info in self.graph["files"].items():
            # Extract module name from path
            # e.g., apps/server/src/core/auth/auth.service.ts -> core/auth/auth.service
            module_name = file_path.replace('\\', '/').rsplit('.', 1)[0]
            module_map[module_name] = file_path

            # Also add shorter aliases
            parts = module_name.split('/')
            for i in range(len(parts)):
                alias = '/'.join(parts[i:])
                if alias not in module_map:
                    module_map[alias] = file_path

        # Resolve imports to actual files
        for file_path, file_info in self.graph["files"].items():
            for imported_module in file_info["imports"]:
                # Skip external modules (npm packages)
                if imported_module.startswith('.') or imported_module.startswith('@'):
                    # Resolve relative imports
                    resolved_path = self._resolve_import(file_path, imported_module, module_map)

                    if resolved_path and resolved_path in self.graph["files"]:
                        # Add to relationship graph
                        self.graph["relationships"]["imports"].append({
                            "from": file_path,
                            "to": resolved_path,
                            "module": imported_module
                        })

                        # Update dependents
                        if file_path not in self.graph["files"][resolved_path]["dependents"]:
                            self.graph["files"][resolved_path]["dependents"].append(file_path)

    def _resolve_import(self, file_path: str, imported_module: str, module_map: Dict) -> Optional[str]:
        """Resolve relative import to actual file path"""
        if imported_module.startswith('.'):
            # Relative import
            base_dir = str(Path(file_path).parent)

            # Resolve the import path
            if imported_module.startswith('./'):
                resolved = Path(base_dir) / imported_module[2:]
            elif imported_module.startswith('../'):
                resolved = Path(base_dir) / imported_module
            else:
                resolved = Path(base_dir) / imported_module

            # Normalize the path
            try:
                resolved = resolved.resolve().relative_to(self.root_dir)
            except ValueError:
                return None

            # Try common extensions
            for ext in ['.ts', '.tsx', '.js', '.jsx', '/index.ts', '/index.tsx', '/index.js', '/index.jsx']:
                candidate = str(resolved) + ext
                if candidate in self.graph["files"]:
                    return candidate

                # Also try without adding extension (in case it's already there)
                if str(resolved) in self.graph["files"]:
                    return str(resolved)

        elif imported_module.startswith('@'):
            # Package alias (like @docmost/editor-ext)
            # Try to map to packages directory
            if '@docmost/' in imported_module:
                package_name = imported_module.replace('@docmost/', '')
                # Try to find in packages/
                for candidate_path, candidate_info in self.graph["files"].items():
                    if f'packages/{package_name}' in candidate_path:
                        return candidate_path

        return None

    def save_graph(self, output_path: str):
        """Save dependency graph to JSON file"""
        output_file = Path(output_path)
        output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.graph, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Saved dependency graph to: {output_file}")
        print(f"📦 Graph size: {output_file.stat().st_size / 1024:.2f} KB")


def main():
    print("=" * 60)
    print("DotPrompt Dependency Graph Builder")
    print("=" * 60)

    # Get repository root (parent of .prompt)
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    print(f"\n📁 Repository root: {repo_root}")

    # Build dependency graph
    builder = DependencyGraphBuilder(repo_root)
    graph = builder.build_graph()

    # Save to file
    output_path = script_dir / "dependency-graph.json"
    builder.save_graph(output_path)

    # Print summary
    print("\n📈 Dependency Graph Summary:")
    print(f"   Total files: {graph['metadata']['total_files']}")
    print(f"   Import relationships: {len(graph['relationships']['imports'])}")
    print(f"   Inheritance relationships: {len(graph['relationships']['inheritance'])}")

    print("\n✅ Done!")


if __name__ == "__main__":
    main()
