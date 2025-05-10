# GitHub Setup Guide

This document provides step-by-step instructions for uploading this project to GitHub and sharing it with others.

## Prerequisites

- Git installed on your computer
- GitHub account
- Node.js and npm installed (for frontend)
- Python 3.9+ installed (for backend)

## Steps to Upload to GitHub

1. **Create a new repository on GitHub**

   Go to [GitHub](https://github.com) and create a new repository named "AirportGPT" or any name you prefer.
   Do not initialize it with a README, .gitignore, or license yet.

2. **Configure Git user information (if not already done)**

   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

3. **Add your GitHub repository as a remote**

   ```bash
   git remote add origin https://github.com/yourusername/AirportGPT.git
   ```

4. **Stage all your files**

   ```bash
   git add .
   ```

5. **Commit your changes**

   ```bash
   git commit -m "Initial commit"
   ```

6. **Push to GitHub**

   ```bash
   git push -u origin main
   ```
   
   If your default branch is named "master" instead of "main", use:
   
   ```bash
   git push -u origin master
   ```

## Project Organization

This project has been set up with the following considerations:

1. **Proper .gitignore**: To exclude unnecessary files like `__pycache__`, `node_modules`, etc.
2. **Clear README**: With instructions on how to set up and run the project
3. **Requirements file**: For easy installation of Python dependencies
4. **Package.json**: For running both frontend and backend with a single command

## Running the Project

For developers who clone your repository, they can:

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/AirportGPT.git
   cd AirportGPT
   ```

2. **Install all dependencies (both frontend and backend)**

   ```bash
   npm run install:all
   ```

3. **Run both frontend and backend simultaneously**

   ```bash
   npm run dev
   ```

   This will start the backend server at http://localhost:8002 and the Next.js frontend at http://localhost:3000

4. **Or run them separately**

   ```bash
   # Backend only
   npm run start:backend
   
   # Frontend only
   npm run start:frontend
   ```

## Additional Tips

1. **Consider adding environment variables**: If your project uses API keys or sensitive information, create a `.env.example` file with dummy values as a template.

2. **Add more documentation**: Consider adding more detailed documentation for complex parts of your project.

3. **Add a license**: Choose an appropriate license for your project based on how you want it to be used by others.

4. **Set up GitHub Actions**: For continuous integration/continuous deployment if needed.
