# AI Chat Assistant

## Overview

This is a modern AI chat application built with React and Express, featuring multi-model AI support, real-time conversation management, and a beautiful UI. The application supports integration with OpenAI GPT-4o, Anthropic Claude, and Google Gemini models, with options for web search, image generation, and code execution capabilities.

## System Architecture

### Frontend Architecture
- **Framework**: React with TypeScript
- **UI Framework**: Radix UI components with shadcn/ui styling
- **Styling**: Tailwind CSS with custom design tokens
- **State Management**: TanStack Query for server state management
- **Routing**: Wouter for lightweight client-side routing
- **Build Tool**: Vite for fast development and optimized builds

### Backend Architecture
- **Runtime**: Node.js with Express.js
- **Database**: PostgreSQL with Drizzle ORM
- **Database Provider**: Neon serverless PostgreSQL
- **AI Integration**: Multiple AI providers (OpenAI, Anthropic, Google)
- **Session Management**: Connect-pg-simple for PostgreSQL session storage
- **Development**: Hot module replacement with Vite middleware

### Database Schema
- **Users**: Basic user management with username/password
- **Conversations**: Chat sessions with timestamps and user association
- **Messages**: Individual chat messages with role, content, model, and metadata fields

## Key Components

### Data Storage
- **Primary Database**: PostgreSQL via Neon serverless
- **ORM**: Drizzle ORM for type-safe database operations
- **Fallback Storage**: In-memory storage for development/testing
- **Session Storage**: PostgreSQL-backed session management

### AI Integration
- **OpenAI GPT-4o**: Primary text generation model
- **Anthropic Claude**: Claude Sonnet 4 (latest model as of 2025)
- **Google Gemini**: Gemini 2.5 Flash model
- **Multi-Model Support**: Ability to query multiple models simultaneously
- **Tool Integration**: Web search, image generation, and code analysis

### User Interface
- **Theme Support**: Dark/light mode with system preference detection
- **Responsive Design**: Mobile-first approach with desktop enhancements
- **Real-time Updates**: Automatic conversation and message refresh
- **Rich Message Display**: Markdown support, code highlighting, and tool outputs

## Data Flow

1. **User Authentication**: Simple username/password system (demo mode uses userId: 1)
2. **Conversation Management**: Users can create new conversations or continue existing ones
3. **Message Processing**: 
   - User sends message via chat input
   - Message is stored in database
   - AI model processes the message (with optional tools like web search)
   - AI response is stored and displayed
4. **Real-time Updates**: Frontend polls for new messages and conversations

## External Dependencies

### AI Service APIs
- **OpenAI API**: For GPT-4o completions
- **Anthropic API**: For Claude model access
- **Google Gemini API**: For Gemini model access
- **SerpAPI**: For web search functionality (optional)

### Database Services
- **Neon Database**: Serverless PostgreSQL hosting
- **Environment Variables**: All API keys and database URLs configured via environment

### UI and Styling
- **Radix UI**: Accessible component primitives
- **Tailwind CSS**: Utility-first styling framework
- **Lucide Icons**: Modern icon library

## Deployment Strategy

### Build Process
- **Frontend**: Vite builds React app to `dist/public`
- **Backend**: esbuild bundles Express server to `dist/index.js`
- **Database**: Drizzle migrations applied via `db:push` command

### Environment Configuration
- **Development**: Local development with hot reloading
- **Production**: Bundled deployment with optimized assets
- **Environment Variables**: Database URL and API keys required

### Replit Integration
- **Development Mode**: Integrated with Replit's development environment
- **Error Handling**: Runtime error modal for development
- **Asset Management**: Proper path resolution for Replit environment

## Changelog

```
Changelog:
- July 05, 2025. Initial setup
```

## User Preferences

```
Preferred communication style: Simple, everyday language.
```