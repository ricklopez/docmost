# Docmost Repository Analysis

**Analysis Date:** 2025-11-19
**Repository:** Docmost v0.23.2
**Description:** Open-source collaborative wiki and documentation software

---

## 1. File Classification by Language

### TypeScript Distribution

| Location | File Count | Type | Purpose |
|----------|-----------|------|---------|
| `apps/client/src` | 398 | `.ts`, `.tsx` | React frontend application |
| `apps/server/src` | 273 | `.ts` | NestJS backend application |
| `packages/editor-ext/src` | 71 | `.ts` | Shared TipTap editor extensions |
| `packages/ee` | - | `.ts`, `.tsx` | Enterprise Edition features |

**Total TypeScript Files:** 749+ files

### Other File Types

- **JSON:** Configuration files (`package.json`, `tsconfig.json`, translation files)
- **Markdown:** Documentation (`.md` files)
- **YAML:** Docker Compose, CI/CD configurations
- **CSS/PostCSS:** Styling (Mantine PostCSS preset)

---

## 2. Directory Architecture

### Root Structure

```
docmost/
├── .prompt/                    # DotPrompt workspace (analysis, IR, plan)
├── apps/
│   ├── client/                # Frontend React application
│   └── server/                # Backend NestJS application
├── packages/
│   ├── editor-ext/            # Shared TipTap editor extensions
│   └── ee/                    # Enterprise Edition features
├── patches/                   # pnpm patches for dependencies
├── docker-compose.yml         # Docker orchestration
├── Dockerfile                 # Container image definition
├── nx.json                    # Nx monorepo configuration
├── pnpm-workspace.yaml        # pnpm workspace definition
└── package.json               # Root package configuration
```

### Backend Structure (`apps/server/src`)

```
apps/server/src/
├── core/                      # Core business logic modules
│   ├── auth/                 # Authentication & authorization
│   ├── user/                 # User management
│   ├── workspace/            # Workspace management
│   ├── space/                # Space management
│   ├── page/                 # Page/document management
│   ├── comment/              # Comments on pages
│   ├── attachment/           # File attachments
│   ├── group/                # User groups
│   ├── share/                # Public sharing
│   ├── search/               # Full-text search
│   └── casl/                 # CASL permissions framework
├── database/                  # Database layer
│   ├── migrations/           # Database schema migrations (Kysely)
│   ├── repos/                # Repository pattern implementations
│   ├── services/             # Database services
│   ├── types/                # TypeScript database types (auto-generated)
│   └── pagination/           # Pagination utilities
├── collaboration/             # Real-time collaboration (Hocuspocus)
│   ├── server/               # Standalone collab server
│   ├── extensions/           # Hocuspocus extensions
│   ├── adapter/              # Redis adapter
│   └── listeners/            # Collaboration event listeners
├── integrations/              # External integrations
│   ├── environment/          # Environment configuration
│   ├── storage/              # File storage (S3, local)
│   ├── mail/                 # Email service (SMTP, Postmark)
│   ├── queue/                # Job queue (BullMQ)
│   ├── redis/                # Redis integration
│   ├── security/             # Security features
│   ├── export/               # Export functionality
│   ├── import/               # Import functionality
│   ├── transactional/        # Transactional emails (React Email)
│   ├── telemetry/            # Analytics/telemetry
│   ├── health/               # Health checks
│   └── static/               # Static file serving
├── ws/                        # WebSocket gateway
├── common/                    # Shared utilities
│   ├── decorators/           # Custom decorators
│   ├── guards/               # Auth guards
│   ├── interceptors/         # Request/response interceptors
│   ├── middlewares/          # Express/Fastify middlewares
│   ├── events/               # Event emitter definitions
│   ├── helpers/              # Utility functions
│   ├── logger/               # Logging
│   └── validator/            # Validation helpers
├── ee/                        # Enterprise Edition (separate license)
└── main.ts                    # Application entry point
```

### Frontend Structure (`apps/client/src`)

```
apps/client/src/
├── features/                  # Feature-based modules
│   ├── editor/               # Rich text editor (TipTap)
│   ├── page/                 # Page/document features
│   ├── space/                # Space features
│   ├── auth/                 # Authentication UI
│   ├── user/                 # User profile
│   ├── workspace/            # Workspace settings
│   ├── group/                # Group management
│   ├── comment/              # Comment UI
│   ├── search/               # Search interface
│   ├── share/                # Public sharing
│   ├── attachments/          # File uploads/attachments
│   ├── page-history/         # Page version history
│   ├── home/                 # Home dashboard
│   ├── file-task/            # File import tasks
│   └── websocket/            # WebSocket client
├── pages/                     # Route-level pages
│   ├── auth/                 # Login, signup, forgot password
│   ├── dashboard/            # Main dashboard
│   ├── page/                 # Page view/edit
│   ├── space/                # Space view
│   ├── spaces/               # Space list
│   ├── settings/             # Settings pages
│   └── share/                # Public share view
├── components/                # Reusable components
│   ├── common/               # Generic components
│   ├── layouts/              # Layout components
│   ├── settings/             # Settings-specific components
│   ├── icons/                # Custom icons
│   └── ui/                   # UI library components
├── lib/                       # Shared libraries
│   ├── api-client.ts         # API client (Axios)
│   ├── app-route.ts          # Route definitions
│   ├── config.ts             # App configuration
│   ├── constants.ts          # Constants
│   ├── jotai-helper.ts       # Jotai state helpers
│   ├── local-emitter.ts      # Event emitter
│   ├── time.ts               # Date/time utilities
│   ├── types.ts              # TypeScript types
│   └── utils.tsx             # Utility functions
├── hooks/                     # Custom React hooks
├── ee/                        # Enterprise Edition (separate license)
│   ├── api-key/              # API key management
│   ├── billing/              # Billing/subscription
│   ├── cloud/                # Cloud-specific features
│   ├── comment/              # Advanced comment features
│   ├── licence/              # License management
│   ├── mfa/                  # Multi-factor authentication
│   ├── security/             # Security features
│   ├── components/           # EE components
│   ├── hooks/                # EE hooks
│   └── pages/                # EE pages
├── assets/                    # Static assets
└── main.tsx                   # Application entry point
```

### Packages Structure

```
packages/
├── editor-ext/                # Shared TipTap editor extensions
│   └── src/lib/
│       ├── table/            # Table extension with drag-n-drop
│       ├── image/            # Image handling & upload
│       ├── video/            # Video embedding & upload
│       ├── attachment/       # File attachments
│       ├── comment/          # Inline comments
│       ├── callout/          # Callout blocks
│       ├── details/          # Details/summary blocks
│       ├── embed/            # Embeds (Airtable, Loom, Miro, etc.)
│       ├── excalidraw.ts     # Excalidraw diagrams
│       ├── drawio.ts         # Draw.io diagrams
│       ├── mention.ts        # User mentions
│       ├── link.ts           # Link handling
│       ├── math/             # Math equations (KaTeX)
│       ├── markdown/         # Markdown import/export
│       ├── search-and-replace/ # Search & replace functionality
│       ├── custom-code-block.ts # Code blocks with syntax highlighting
│       └── subpages/         # Subpage navigation
└── ee/                        # Enterprise Edition shared code
```

---

## 3. Frameworks Detected

### Backend Frameworks & Libraries

| Framework/Library | Version | Purpose |
|------------------|---------|---------|
| **NestJS** | 11.1.3 | Backend framework (modular architecture) |
| **Fastify** | via @nestjs/platform-fastify | HTTP server (faster than Express) |
| **Kysely** | 0.28.2 | Type-safe SQL query builder |
| **PostgreSQL** | via `pg` 8.16.0 | Relational database |
| **Redis** | via `ioredis` 5.4.1 | Caching, pub/sub, sessions |
| **BullMQ** | 5.61.0 | Job queue system |
| **Hocuspocus** | 2.15.2 | Real-time collaboration server |
| **Yjs** | 13.6.27 | CRDT for collaborative editing |
| **Passport** | - | Authentication middleware |
| **JWT** | via `jsonwebtoken` | Token-based auth |
| **CASL** | 6.7.3 | Authorization/permissions |
| **Socket.io** | 4.8.1 | WebSocket server |
| **Sharp** | 0.34.3 | Image processing |
| **AWS SDK S3** | 3.701.0 | S3-compatible storage |
| **Nodemailer** | 7.0.3 | Email sending |
| **React Email** | 3.0.2 | Email template rendering |
| **Stripe** | 17.5.0 | Payment processing (EE) |
| **Typesense** | 2.1.0 | Full-text search engine |
| **bcrypt** | 5.1.1 | Password hashing |
| **class-validator** | 0.14.1 | DTO validation |
| **class-transformer** | 0.5.1 | DTO transformation |

### Frontend Frameworks & Libraries

| Framework/Library | Version | Purpose |
|------------------|---------|---------|
| **React** | 18.3.1 | UI framework |
| **Vite** | 6.3.5 | Build tool & dev server |
| **React Router** | 7.0.1 | Client-side routing |
| **Mantine** | 8.1.3 | UI component library |
| **TipTap** | 2.10.3 | Rich text editor (ProseMirror) |
| **TanStack Query** | 5.80.6 | Data fetching & caching |
| **Jotai** | 2.12.5 | Atomic state management |
| **Axios** | 1.9.0 | HTTP client |
| **Socket.io Client** | 4.8.1 | WebSocket client |
| **Hocuspocus Provider** | 2.15.2 | Real-time collaboration provider |
| **Yjs** | 13.6.27 | CRDT for collaborative editing |
| **CASL React** | 4.0.0 | Authorization in React |
| **i18next** | 23.14.0 | Internationalization |
| **Zod** | 3.25.56 | Schema validation |
| **Excalidraw** | 0.18.0 | Diagram drawing |
| **Mermaid** | 11.11.0 | Diagram rendering |
| **KaTeX** | 0.16.22 | Math equation rendering |
| **Lowlight** | 3.3.0 | Code syntax highlighting |
| **PostHog** | 1.255.1 | Product analytics |
| **React Arborist** | 3.4.0 | Tree view component |

### Monorepo & Build Tools

| Tool | Version | Purpose |
|------|---------|---------|
| **Nx** | 20.4.5 | Monorepo orchestration |
| **pnpm** | 10.4.0 | Package manager |
| **TypeScript** | 5.7.2/5.7.3 | Type system |
| **ESLint** | 9.x | Linting |
| **Prettier** | 3.x | Code formatting |

---

## 4. Backend / Frontend / Shared Boundaries

### Backend (`apps/server`)

**Responsibility:** API server, database operations, business logic, real-time collaboration

**Key Modules:**
- REST API endpoints (11 controllers, 79+ endpoints)
- WebSocket gateway for real-time notifications
- Standalone collaboration server (Hocuspocus)
- Database repositories using Kysely ORM
- Job queue processors (BullMQ)
- Authentication & authorization (JWT, CASL)
- File storage (S3, local)
- Email service (transactional emails)
- Full-text search (Typesense, PostgreSQL)
- SSO integrations (SAML, OIDC, LDAP, Google OAuth)

**Technologies:** NestJS, Fastify, PostgreSQL, Redis, Hocuspocus, Yjs

### Frontend (`apps/client`)

**Responsibility:** User interface, client-side routing, state management, editor UI

**Key Modules:**
- Rich text editor with TipTap extensions
- Real-time collaboration UI
- Page/space navigation
- User settings & workspace management
- Authentication flows
- Search interface
- Comments & mentions UI
- File uploads & attachments
- Diagram editors (Excalidraw, Draw.io)
- Public share views

**Technologies:** React, Vite, Mantine UI, TipTap, Hocuspocus Provider, Jotai, TanStack Query

### Shared (`packages/editor-ext`)

**Responsibility:** TipTap editor extensions used by both client and server

**Key Extensions:**
- Table with drag-and-drop
- Image/video/attachment uploads
- Inline comments
- Callouts, details/summary blocks
- Embeds (Airtable, Loom, Miro, etc.)
- Math equations (KaTeX)
- Code blocks with syntax highlighting
- Markdown import/export
- Mentions, links
- Diagrams (Excalidraw, Draw.io)
- Subpage navigation
- Search & replace

**Why Shared?**
- Server uses these extensions to render HTML from page content
- Client uses these extensions in the editor UI
- Ensures consistent rendering between server and client

### Enterprise Edition (`packages/ee`, `apps/*/src/ee`)

**Responsibility:** Enterprise-only features under separate license

**Modules:**
- API key management
- Billing & subscriptions (Stripe)
- Multi-factor authentication (MFA)
- Advanced security features
- Cloud-specific features
- License management

**License:** Docmost Enterprise License (separate from AGPL 3.0)

---

## 5. Domain Models and Business Logic

### Core Domain Entities (from `apps/server/src/database/types/db.d.ts`)

#### **Workspace**
- Multi-tenant root entity
- Contains users, groups, spaces, pages
- License key management
- Billing integration

#### **User**
- Authentication (email/password, SSO)
- Roles: `owner`, `admin`, `member`, `guest`
- Profile (name, avatar, locale, timezone)
- MFA support

#### **Group**
- User grouping for permissions
- Many-to-many relationship with users
- Used in permission grants

#### **Space**
- Document organization container
- Permissions management (viewer, commenter, writer, admin, owner)
- Settings (slug, icon, description)
- Parent-child relationships (subspaces)

#### **Page**
- Core document entity
- Hierarchical (parent-child relationships)
- Slug-based URLs
- Content stored as JSON (ProseMirror)
- Full-text search (PostgreSQL tsvector)
- Trash/soft delete support
- Cover image support
- Contributor tracking

#### **PageHistory**
- Version history for pages
- Stores content snapshots
- Creator and timestamp tracking

#### **Comment**
- Inline and block comments on pages
- Thread support
- Resolved/unresolved status
- Position tracking in document

#### **Attachment**
- File uploads
- Image, video, document support
- Full-text search (for PDFs, DOCX, etc.)
- Size limits
- Workspace and page association

#### **Share**
- Public sharing of pages
- Password protection
- Expiration dates
- Access tracking

#### **AuthProvider**
- SSO configuration (SAML, OIDC, LDAP, Google)
- Per-workspace SSO settings
- Group synchronization

#### **ApiKey**
- API authentication
- Scoped to workspace
- Expiration support

#### **Backlink**
- Page-to-page references
- Automatic backlink tracking

#### **FileTask**
- Import job tracking
- Status monitoring (pending, processing, completed, failed)

### Business Logic Patterns

#### **Repository Pattern**
- All database operations go through repository classes
- Located in `apps/server/src/database/repos/`
- Repositories per entity: `PageRepo`, `UserRepo`, `SpaceRepo`, etc.
- Kysely query builder for type-safe SQL

#### **Service Layer**
- Business logic in `*.service.ts` files
- Services coordinate repositories, events, and external integrations
- Example: `PageService` handles page CRUD, permissions, search indexing

#### **Controller Layer**
- REST API endpoints in `*.controller.ts` files
- DTO validation with `class-validator`
- Guards for authentication and authorization
- Example: `PageController` exposes page API endpoints

#### **Event-Driven Architecture**
- Event emitters for cross-module communication
- Listeners in `database/listeners/` and `collaboration/listeners/`
- Example: `PageListener` updates backlinks when pages change

#### **Job Queue**
- BullMQ for async processing
- Processors in `integrations/*/processors/`
- Examples: email sending, file imports, backlink updates, attachment indexing

#### **Permissions (CASL)**
- Ability factories in `core/casl/abilities/`
- Fine-grained permissions: `read`, `create`, `update`, `delete`, `manage`
- Space-level and workspace-level permissions
- Role-based access control

---

## 6. API Endpoints

### Endpoint Summary (79+ endpoints across 11 controllers)

| Controller | Endpoints | Modules |
|------------|-----------|---------|
| **AuthController** | 8 | Login, signup, logout, password reset, MFA |
| **UserController** | 2 | User profile, user list |
| **WorkspaceController** | 15 | Workspace settings, invitations, members |
| **SpaceController** | 9 | Space CRUD, permissions, members |
| **PageController** | 14 | Page CRUD, move, trash, history, export |
| **CommentController** | 5 | Comment CRUD, resolve |
| **AttachmentController** | 6 | Upload, download, delete |
| **ShareController** | 8 | Public sharing, password protection |
| **GroupController** | 8 | Group CRUD, members |
| **SearchController** | 3 | Full-text search (pages, attachments) |
| **ShareSeoController** | 1 | SEO for public shares |

### Example Endpoints

#### Authentication (`/api/auth/*`)
- `POST /api/auth/signup` - User signup
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `POST /api/auth/forgot-password` - Password reset request
- `POST /api/auth/reset-password` - Reset password with token

#### Pages (`/api/pages/*`)
- `GET /api/pages/:id` - Get page by ID
- `POST /api/pages` - Create new page
- `PATCH /api/pages/:id` - Update page content
- `DELETE /api/pages/:id` - Delete page (soft delete)
- `POST /api/pages/:id/move` - Move page to different space/parent
- `GET /api/pages/:id/history` - Get page version history
- `POST /api/pages/:id/export` - Export page (Markdown, HTML, PDF)

#### Spaces (`/api/spaces/*`)
- `GET /api/spaces` - List all spaces
- `POST /api/spaces` - Create new space
- `PATCH /api/spaces/:id` - Update space settings
- `DELETE /api/spaces/:id` - Delete space
- `GET /api/spaces/:id/members` - Get space members
- `POST /api/spaces/:id/members` - Add space member

#### Search (`/api/search/*`)
- `GET /api/search/pages` - Full-text search pages
- `GET /api/search/attachments` - Search attachments

### API Client Pattern (Frontend)

**Location:** `apps/client/src/lib/api-client.ts`

- Axios-based HTTP client
- JWT token injection via interceptors
- Error handling and retry logic
- Base URL configuration
- Cookie-based auth token storage

---

## 7. Prompt/Agent Infrastructure

**Result:** No AI/LLM infrastructure detected.

**Analysis:**
- Grep search for AI/LLM-related keywords returned false positives (e.g., "email", "domain")
- No evidence of:
  - OpenAI, Anthropic, or other LLM API integrations
  - Prompt templates or prompt engineering
  - AI-powered features (summarization, generation, etc.)
  - Vector databases (e.g., Pinecone, Weaviate)
  - Embedding models

**Conclusion:** Docmost is a traditional collaborative wiki/documentation platform without AI/agent capabilities.

---

## 8. Recommended DotPrompt Plan Structure

Based on the repository analysis, here is the recommended structure for the `.prompt/plan/` directory:

### Plan Layer Organization

```
.prompt/plan/
├── app/
│   ├── server/
│   │   ├── core/
│   │   │   ├── auth.plan.md          # Auth module architecture
│   │   │   ├── user.plan.md          # User management
│   │   │   ├── workspace.plan.md     # Workspace management
│   │   │   ├── space.plan.md         # Space management
│   │   │   ├── page.plan.md          # Page/document management
│   │   │   ├── comment.plan.md       # Comments system
│   │   │   ├── attachment.plan.md    # File attachments
│   │   │   ├── group.plan.md         # User groups
│   │   │   ├── share.plan.md         # Public sharing
│   │   │   ├── search.plan.md        # Full-text search
│   │   │   └── casl.plan.md          # Permissions framework
│   │   ├── collaboration/
│   │   │   ├── hocuspocus.plan.md    # Real-time collab server
│   │   │   ├── yjs-integration.plan.md
│   │   │   └── persistence.plan.md   # Collaboration persistence
│   │   ├── integrations/
│   │   │   ├── storage.plan.md       # S3/local storage
│   │   │   ├── mail.plan.md          # Email service
│   │   │   ├── queue.plan.md         # Job queue (BullMQ)
│   │   │   ├── redis.plan.md         # Redis integration
│   │   │   ├── security.plan.md      # Security features
│   │   │   ├── export.plan.md        # Export functionality
│   │   │   ├── import.plan.md        # Import functionality
│   │   │   └── telemetry.plan.md     # Analytics
│   │   ├── websocket/
│   │   │   └── ws-gateway.plan.md    # WebSocket notifications
│   │   └── api-overview.plan.md      # Overall API architecture
│   ├── client/
│   │   ├── features/
│   │   │   ├── editor.plan.md        # TipTap editor integration
│   │   │   ├── page.plan.md          # Page UI features
│   │   │   ├── space.plan.md         # Space UI features
│   │   │   ├── auth.plan.md          # Auth UI flows
│   │   │   ├── user.plan.md          # User profile UI
│   │   │   ├── workspace.plan.md     # Workspace settings UI
│   │   │   ├── group.plan.md         # Group management UI
│   │   │   ├── comment.plan.md       # Comment UI
│   │   │   ├── search.plan.md        # Search UI
│   │   │   ├── share.plan.md         # Public sharing UI
│   │   │   ├── attachments.plan.md   # File upload UI
│   │   │   └── websocket.plan.md     # Real-time updates UI
│   │   ├── state-management/
│   │   │   ├── jotai.plan.md         # Global state (Jotai)
│   │   │   └── tanstack-query.plan.md # Server state (TanStack Query)
│   │   ├── routing/
│   │   │   └── react-router.plan.md  # Client-side routing
│   │   └── ui-overview.plan.md       # UI architecture overview
│   └── integration/
│       ├── auth-flow.plan.md         # End-to-end auth flow
│       ├── collaboration-flow.plan.md # Real-time collab flow
│       ├── page-lifecycle.plan.md    # Page CRUD flow
│       └── permissions-flow.plan.md  # Permission checking flow
├── db/
│   ├── schema/
│   │   ├── workspaces.plan.md        # Workspace schema
│   │   ├── users.plan.md             # User schema
│   │   ├── groups.plan.md            # Group schema
│   │   ├── spaces.plan.md            # Space schema
│   │   ├── pages.plan.md             # Page schema
│   │   ├── page-history.plan.md      # Page history schema
│   │   ├── comments.plan.md          # Comment schema
│   │   ├── attachments.plan.md       # Attachment schema
│   │   ├── shares.plan.md            # Share schema
│   │   ├── auth-providers.plan.md    # SSO providers schema
│   │   ├── api-keys.plan.md          # API keys schema
│   │   ├── backlinks.plan.md         # Backlinks schema
│   │   └── file-tasks.plan.md        # Import tasks schema
│   ├── migrations/
│   │   └── migration-strategy.plan.md # Migration approach
│   ├── repositories/
│   │   └── repository-pattern.plan.md # Repository pattern design
│   └── database-architecture.plan.md # Overall DB architecture
├── shared/
│   ├── editor-extensions/
│   │   ├── table.plan.md             # Table extension
│   │   ├── image.plan.md             # Image extension
│   │   ├── video.plan.md             # Video extension
│   │   ├── attachment.plan.md        # Attachment extension
│   │   ├── comment.plan.md           # Comment extension
│   │   ├── callout.plan.md           # Callout extension
│   │   ├── embed.plan.md             # Embed extension
│   │   ├── excalidraw.plan.md        # Excalidraw extension
│   │   ├── drawio.plan.md            # Draw.io extension
│   │   ├── math.plan.md              # Math extension
│   │   ├── markdown.plan.md          # Markdown import/export
│   │   └── mention.plan.md           # Mention extension
│   ├── types/
│   │   └── shared-types.plan.md      # Shared TypeScript types
│   └── editor-ext-overview.plan.md   # Editor extensions overview
├── enterprise/
│   ├── api-keys.plan.md              # API key management (EE)
│   ├── billing.plan.md               # Billing & subscriptions (EE)
│   ├── mfa.plan.md                   # Multi-factor auth (EE)
│   ├── security.plan.md              # Advanced security (EE)
│   └── license.plan.md               # License management (EE)
└── architecture/
    ├── monorepo.plan.md              # Nx monorepo architecture
    ├── deployment.plan.md            # Docker & deployment
    ├── scalability.plan.md           # Scaling strategy
    ├── security.plan.md              # Security architecture
    └── testing.plan.md               # Testing strategy
```

### Plan File Template

Each `*.plan.md` file should follow this structure:

```markdown
# [Module Name] Architecture Plan

## Overview
- Purpose and scope
- Key responsibilities
- Dependencies

## Components
- List of files/classes
- Component relationships
- Data flow

## API Surface
- Public interfaces
- Endpoints (if applicable)
- Events emitted/consumed

## Database Schema
- Tables affected
- Relationships
- Indexes

## Business Logic
- Key algorithms
- Validation rules
- State transitions

## Integration Points
- Upstream dependencies
- Downstream consumers
- External services

## Migration Strategy
- Changes required
- Risks and mitigation
- Testing approach

## Dependencies
- Internal modules
- External libraries
- Infrastructure requirements
```

### DotPrompt Workflow

1. **Analysis Phase** (`.prompt/analysis/`)
   - Repository structure analysis ✓ (this document)
   - Dependency graph generation (future)
   - Semantic index generation (future)

2. **IR Phase** (`.prompt/ir/`)
   - Generate IR for each source file using the 14-section template
   - Store in directory structure mirroring source: `.prompt/ir/apps/server/src/core/auth/auth.service.ts.md`
   - Tag and classify each file

3. **Plan Phase** (`.prompt/plan/`)
   - Generate architecture blueprints per module
   - Define migration strategies
   - Document component relationships

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| **Total TypeScript Files** | 749+ |
| **Backend Files** | 273 |
| **Frontend Files** | 398 |
| **Shared Package Files** | 71 |
| **Database Tables** | 15+ core tables |
| **API Endpoints** | 79+ REST endpoints |
| **NestJS Modules** | 20+ modules |
| **Controllers** | 11 controllers |
| **Services** | 16+ services |
| **Repositories** | 11+ repositories |
| **Database Migrations** | 20+ migrations |
| **Frontend Features** | 13+ feature modules |
| **UI Pages** | 6+ page categories |

---

## Technology Stack Summary

**Monorepo:** Nx, pnpm workspaces
**Backend:** NestJS, Fastify, PostgreSQL, Kysely, Redis, BullMQ
**Frontend:** React, Vite, Mantine UI, TanStack Query, Jotai
**Editor:** TipTap (ProseMirror)
**Real-time:** Hocuspocus, Yjs, Socket.io, Redis
**Storage:** S3-compatible, local filesystem
**Search:** Typesense, PostgreSQL full-text search
**Auth:** JWT, Passport, CASL, SSO (SAML, OIDC, LDAP, Google)
**Email:** Nodemailer, React Email
**Payments:** Stripe (EE)
**Deployment:** Docker, Docker Compose

---

## Next Steps for DotPrompt IR Generation

1. **Generate Dependency Graph**
   - Map all import/export relationships
   - Store in `.prompt/analysis/dependency-graph.json`

2. **Generate IR Files**
   - For each TypeScript file, create IR using the 14-section template
   - Start with critical paths: auth → workspace → space → page
   - Use dependency graph to populate `dependsOn` and `usedBy` sections

3. **Generate Plan Files**
   - Group related IR files into module plans
   - Define migration strategies per module
   - Document integration points between modules

4. **Semantic Indexing**
   - Extract tags from all IR files
   - Build semantic index for searchability
   - Store in `.prompt/analysis/semantic-index.md`

---

**Analysis Complete.**
