# Discord Role Assignment Bot

## Overview

This is a Discord bot built with discord.py that provides an interactive role assignment system for new server members. The bot displays role selection buttons when members join, allowing them to choose from predefined roles like Gamer, Music Lover, Reader, Developer, and Artist. The system uses Discord's modern UI components with persistent views and button interactions to create a user-friendly onboarding experience.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Bot Framework
- **Discord.py with Commands Extension**: Uses the discord.py library with the commands extension for structured command handling and event processing
- **Intent-based Architecture**: Configured with specific intents (members, message_content) to handle member join events and command processing
- **Asynchronous Event Handling**: Built on Python's asyncio framework for handling concurrent Discord interactions

### Role Management System
- **Button-based UI**: Implements Discord UI views with interactive buttons for role selection
- **Predefined Role Mapping**: Uses a dictionary structure to map emoji indicators to role names for easy configuration
- **View Timeout Management**: 30-minute timeout on role selection views to prevent resource leaks

### Configuration Management
- **Environment Variables**: Uses python-dotenv for secure token management
- **Customizable Role System**: Centralized AVAILABLE_ROLES dictionary allows easy modification of available roles
- **Command Prefix**: Configurable command prefix system (currently set to '!')

### Event-Driven Architecture
- **Member Join Detection**: Listens for new member join events to trigger role assignment interface
- **Interaction Response System**: Handles button click interactions for role assignment
- **Persistent Views**: Role selection interface remains active for extended periods

## External Dependencies

### Core Libraries
- **discord.py**: Primary Discord API wrapper library for bot functionality
- **python-dotenv**: Environment variable management for secure configuration

### Discord Platform Integration
- **Discord Gateway API**: Real-time event streaming for member joins and interactions
- **Discord REST API**: HTTP-based API for role management and message sending
- **Discord UI Components**: Native button and view components for interactive interfaces

### Runtime Environment
- **Python 3.8+**: Required runtime environment
- **Discord Bot Token**: Authentication token from Discord Developer Portal
- **Server Permissions**: Requires "Manage Roles" permission in Discord servers