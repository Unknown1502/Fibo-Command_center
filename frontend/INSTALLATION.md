# Frontend Installation Guide

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager

## Installation Steps

### Option 1: Using Command Prompt (Recommended for Windows)

1. Open Command Prompt (cmd.exe)
2. Navigate to frontend directory:
   ```
   cd "C:\Users\prajw\OneDrive\Desktop\Research folders\FIBO Hackathon\fibo-command-center\frontend"
   ```
3. Install dependencies:
   ```
   npm install
   ```

### Option 2: Using PowerShell (Requires Execution Policy Change)

If you prefer PowerShell, you need to allow script execution:

1. Open PowerShell as Administrator
2. Run:
   ```
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
3. Confirm with 'Y'
4. Then navigate and install:
   ```
   cd "C:\Users\prajw\OneDrive\Desktop\Research folders\FIBO Hackathon\fibo-command-center\frontend"
   npm install
   ```

### Option 3: Manual Installation via File Explorer

1. Open File Explorer
2. Navigate to: `C:\Users\prajw\OneDrive\Desktop\Research folders\FIBO Hackathon\fibo-command-center\frontend`
3. Type `cmd` in the address bar and press Enter
4. In the Command Prompt window that opens, run:
   ```
   npm install
   ```

## After Installation

Once dependencies are installed, you can start the development server:

```bash
npm start
```

This will:
- Start the React development server on http://localhost:3000
- Enable hot reloading for development
- Open the application in your default browser

## Build for Production

To create an optimized production build:

```bash
npm run build
```

The build files will be in the `build/` directory.

## Troubleshooting

### PowerShell Script Execution Error
If you see "running scripts is disabled on this system", use Command Prompt instead or change the execution policy as shown in Option 2.

### Port Already in Use
If port 3000 is already in use, the CLI will prompt you to use another port (usually 3001).

### Module Not Found Errors
If you encounter module errors after installation, try:
```bash
rm -rf node_modules package-lock.json
npm install
```
