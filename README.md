# Fjomp - Inventory & Service Management System

A comprehensive Flask-based web application for managing customers, inventory parts, delivery notes, installation reports (IR), and service operations.

## Overview

Fjomp is an internal business management system designed for tracking customer equipment, managing parts inventory, generating delivery notes, and creating installation/service reports. The application connects to a Microsoft SQL Server database and provides a web interface for technicians and administrators.

## Features

### Core Modules

- **Customer Management** (`customers.py`)
  - Customer database with unit tracking
  - Equipment installation and warranty management
  - Unit charge modes and replacement dates
  - Customer-specific unit assignment

- **Parts Management** (`parts.py`)
  - Parts inventory with pricing tiers (9 price groups)
  - Stock tracking and location management
  - Vendor and category organization
  - Bulk import functionality from external systems

- **Delivery Notes** (`delivnotes.py`)
  - Create and manage delivery notes
  - PDF generation for delivery documentation
  - Email delivery note functionality
  - Price group selection per customer
  - Track shipped/unshipped deliveries

- **Installation Reports (IR)** (`ir.py`)
  - Service and installation documentation
  - Unit and parts tracking per job
  - PDF report generation
  - Historical record keeping

- **Swap-outs** (`swapouts.py`)
  - Equipment swap/replacement tracking
  - Unit exchange documentation

- **Lookup** (`lookup.py`)
  - Search functionality across the system
  - Quick access to customers, parts, and units

- **Settings** (`settings.py`)
  - User management
  - System configuration
  - Bug reporting system
  - Password management

## Technology Stack

- **Backend**: Python 3 with Flask
- **Database**: Microsoft SQL Server (via pyodbc)
- **Frontend**: HTML templates with vanilla JavaScript
- **Styling**: Custom CSS with light/dark theme support
- **PDF Generation**: HTML-to-PDF rendering

## Prerequisites

- Python 3.x
- Microsoft SQL Server with ODBC Driver 17
- Access to the `winstat` database on server `P2019\WSData`

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Fjomp
```

2. Install required Python packages:
```bash
pip install flask pyodbc
```

3. Ensure ODBC Driver 17 for SQL Server is installed on your system.


## Running the Application

### Development Mode

```bash
python main.py
```

The application will start on `http://0.0.0.0:80` (requires admin/root privileges for port 80).

### Production Mode

Uncomment the Waitress server configuration in `main.py`:

```python
from waitress import serve
serve(app, host="0.0.0.0", port="80")
```

## Project Structure

```
Fjomp/
├── main.py              # Main application controller and entry point
├── customers.py         # Customer management module
├── parts.py            # Parts inventory module
├── delivnotes.py       # Delivery notes module
├── ir.py               # Installation reports module
├── swapouts.py         # Equipment swap-out module
├── lookup.py           # Search functionality module
├── settings.py         # Settings and configuration module
├── models.csv          # Equipment models reference
├── static/             # Static assets (CSS, JS, images)
│   ├── *.css          # Stylesheets (light/dark themes)
│   ├── *.js           # Client-side JavaScript
│   ├── bugs/          # Bug tracking directory
│   ├── DB/            # Database-related files
│   └── pictures/      # Image assets
└── templates/          # HTML templates
    ├── landing.html   # Main dashboard
    ├── login.html     # Login page
    ├── customers.html # Customer management interface
    ├── delivnotes.html# Delivery notes interface
    ├── ir.html        # Installation reports interface
    └── ...            # Other templates
```

## Authentication

The system uses a custom authentication mechanism:

1. First-time login sets a password for the technician
2. Subsequent logins validate against stored passwords
3. Session management via cookies
4. Authorized users list maintained in `static/authuser.csv`

## Key Features

### Theme Support
- Light and dark themes
- Theme preference stored in cookies
- Consistent styling across all modules

### Import Functionality
- Bulk import parts from external systems
- Automatic price tier updates
- Stock level synchronization
- Inactive part flagging

### PDF Generation
- Delivery note PDFs
- Installation report PDFs
- Swap-out documentation

### Status Tracking
- Technician availability status (Level 3 status)
- Color-coded status indicators (red, yellow, green, blue)
- Real-time status updates

## Database Schema

The application expects the following main tables in the SQL Server database:

- `Technicians` - User accounts and authentication
- `Customers` - Customer information
- `Units` - Equipment/units assigned to customers
- `Parts` - Inventory parts with pricing
- `DeliveryNotes` - Delivery documentation
- `IR` - Installation reports
- `SwapOuts` - Equipment swap records

## Security Considerations

⚠️ **Important**: This application contains hardcoded database credentials and should only be used in a secure, internal network environment. For production use, consider:

- Moving credentials to environment variables
- Implementing proper password hashing
- Adding HTTPS support
- Implementing CSRF protection
- Adding input validation and SQL injection prevention

## Development

### Adding New Features

1. Create a new module file (e.g., `newfeature.py`)
2. Import it in `main.py`
3. Add routes using Flask decorators
4. Create corresponding templates in `templates/`
5. Add styling in `static/`

### Database Queries

Use the `sql()` helper function for database operations:

```python
# SELECT query
results = sql("SELECT", "SELECT * FROM TableName")

# INSERT/UPDATE query
sql("INSERT", "INSERT INTO TableName VALUES (...)")
```

## Bug Tracking

The application includes a built-in bug tracking system:
- Bug reports stored in `static/bugs/`
- Completed bugs moved to `static/bugs/!klara/`
- Bug viewing interface in login page

## License

[Specify your license here]

## Support

For issues or questions, please contact the development team or submit a bug report through the application's bug tracking system.
