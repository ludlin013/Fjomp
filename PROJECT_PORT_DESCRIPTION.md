# Fjomp Project Analysis & Migration Plan

## Executive Summary
Fjomp is a legacy internal business management system built with Flask and Vanilla JavaScript, relying on a Microsoft SQL Server database. The system manages customer equipment, parts inventory, delivery notes, and provides modules for swap-outs and installation reports (IR). The objective is to migrate this application to a modern architecture using a Python-based backend API and a Vite-based frontend GUI structure, seamlessly preserving functionality and User Experience (UX) while modernizing security, maintainability, and codebase responsiveness.

## 1. Current Architecture & State
* **Backend Framework:** Python 3 + Flask (monolithic design).
* **Frontend Framework:** Vanilla HTML, CSS, JavaScript rendered via Jinja2/Flask templates (`render_template`).
* **Database:** Microsoft SQL Server (connected via raw `pyodbc`).
* **Authentication/State:** Cookie-based session tracking (`request.cookies.get`). Custom login checks against a `Technicians` table and authorized texts in `static/authuser.csv`.
* **State Management:** High reliance on HTML data injection utilizing Jinja2, with logic relying heavily on frontend vanilla JS querying standard DOM elements. State per feature/user is often saved via web cookies continually parsed on subsequent requests (e.g., `custtable` dictating the current active tab, `theme` tracking current color schema).
* **Security Structure:** The current app uses string concatenation for SQL statements `sql("INSERT", "UPDATE... '"+val+"'")`, extensively exposing the application to SQL injections.
* **Bug Tracking/Storage:** Local filesystem is leveraged contextually (e.g., issues logged locally into `static/bugs/` files, offline units stored into `static/units.csv`).

## 2. Functionality & Core Modules
1. **Landing/Status (`main.py` & `landing.html`):** User dashboard showing current users online, their "levels/availability", via interactive color codes.
2. **Customers (`customers.py` & `customers.html`):** Extensive CRUD operations filtering active customer accounts and their nested entities (equipment). Divides view-states utilizing tables (tabs for IR history, Delivery Notes, Swap-outs, active hardware units).
3. **Parts & Inventory (`parts.py` & `parts.html`):** Reads CSV imports and manages parts stock, pricing variants (using up to 9 custom tier price levels), categories, and sorting mechanics.
4. **Delivery Notes (`delivnotes.py` & `delivnotes.html`):** Logistics management of delivery documents, categorizing what is functionally shipped vs. unshipped. Includes PDF/email handling capabilities mapping data back to the relevant client/hardware item.
5. **Installation Reports / IR (`ir.py` & `ir.html`):** Generates service documentation/reports for jobs. Output is rendered via dynamically built HTML-to-PDF files (`irdpdf.html` etc.).
6. **Swap-outs (`swapouts.py`):** Equipment returns, Return Merchandise Authorization (RMA) management, and unit lifecycle phase mapping (e.g., mapping `0:"Ingen åtgärd", 2:"Skickad till kund"`...).
7. **Lookup (`lookup.py`):** Broad search operations indexing fields globally across other data tables in real-time.
8. **Settings (`settings.py`):** Settings configurator allowing application variables updates, users creation routines, alongside password alterations.

## 3. Recommended Migration Architecture

### 3.1 Backend (Python REST API only)
The monolithic Flask app will be refactored into a Headless RESTful API responding to the Vite Frontend logic asynchronously:
* **Framework Recommendation:** **FastAPI** is recommended due to automatic Swagger UI documentation generation, performance optimizations, and strict data-type safety validations using Pydantic. Alternatively, standardizing a **Flask API**.
* **Database Access (ORM):** Exchanging raw `pyodbc` concatenations into robust **SQLAlchemy** or **SQLModel** architectures. This permanently sanitizes endpoints preventing SQL injections and vastly refactors massive queries inside `customers.py` into readable objects. The underlying driver can persist as `pyodbc` since the server holds Microsoft SQL constructs.
* **Authentication Workflow:** Replace the unsecured cookie-based plaintext verification endpoints with robust **JWT (JSON Web Tokens)** mechanisms or secure HTTP-Only session hashing.
* **Endpoint Topology Mapping:** Flask `app.route(...)` HTML resolvers will transmute into pure JSON handling structures. 
  * Example: Re-resolving `/customers?customer=id` into `GET /api/customers/{id}`. Sub-relational views into `GET /api/customers/{id}/units`.

### 3.2 Frontend (Vite)
* **Build tool & Framework:** The User interface will be configured with **Vite**. The explicit framework depends on engineering preferences, but **React**, **Vue 3**, or **Svelte** is optimal. Since preserving current UX/UI designs was explicitly requested: Vanilla js structure can be implemented via Vite compilation tools mapping directly to `index.html`.
* **State Management:** Abstract backend cookies (`theme`, `custtable`, `custsort`) into global state Contexts, Redux/Pinia/Zustand, or LocalStorage API bindings. 
* **Routing logic:** Incorporating a frontend router (e.g. `Vue Router`, `React-Router-Dom`) overriding default browser refreshes, dynamically refreshing inner content layout blocks per module (/landing -> /customers).
* **Styling:** CSS files populated inside `static/*.css` layouts (such as `customers.css`) can be entirely copy-pasted and adapted as standard module assets/Tailwind/CSS injections, preserving exact UX styling, margins, colors, and the native Light/Dark themes.
* **PDF Documentation Generation:** Instead of the Flask backend doing inline HTML generation to serve PDF renders, logic can pivot. Solutions: 1) Client renders using elements mapping inside standard `jspdf`/`html2pdf.js` configurations or 2) A standalone micro-controller inside the Python backend that constructs the PDF binaries returning standard payloads mapping to browser download blobs. 

## 4. Execution Roadmap Strategy

### Phase 1: Preparation & Scaffolding
1. Scaffold Python API backend environment parameters (Fastapi/Flask module structuring).
2. Configure base database ORM relationships linking back to the `P2019\WSData` system.
3. Establish Security (Login logic + JWT endpoint).
4. Init the Vite workspace environment.

### Phase 2: System API Migration
1. Re-map explicit `SELECT` queries across all logic sections (`ir.py`, `customers.py` etc) into JSON response models.
2. Refactor all active mutations (`UPDATE`/`INSERT`/`DELETE`) to HTTP methodology `POST/PUT/DELETE` routers safeguarding user-given inputs.
3. Refactor internal utility files `csv_imports`, `storage/bugs` routing.

### Phase 3: Frontend Interface Construction
1. Deploy core Navigation systems and global state (Authorization verification contexts + Dark/Light Theme global wrappers).
2. Sequentially build interfaces mirroring layout logic: `Customers`, `Parts`, `IR`, `Deliveries`.
3. Connect User interface interaction handlers dynamically triggering to the newly established REST API architecture.

### Phase 4: Finalization & Quality Assurance
1. Comprehensive testing that exact legacy operations flow matches (ensuring `Swap-out status arrays`, `Price filtering loops`, `Technician active statuses` resolve cleanly).
2. Adapt document generation components for the PDF deliverables (`Delivery Notes` / `IR`).
3. Clean out legacy template Jinja codes.
