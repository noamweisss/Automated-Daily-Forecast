# GEMINI.md

## Project Purpose and Functionality

This project automates the creation of daily weather forecast images for the Israel Meteorological Service (IMS). It is a Python application designed to be run as a daily scheduled task, generating visually appealing and informative Instagram stories.

The core functionality of the application is to:

1.  **Fetch Data:** Download the latest weather forecast data from the IMS website, which is provided in XML format with ISO-8859-8 encoding.
2.  **Process Data:** Convert the XML data to UTF-8, parse it, and extract the relevant forecast information for 15 major Israeli cities.
3.  **Generate Image:** Create a 1080x1920 image (Instagram story format) that displays the weather forecast for all 15 cities, sorted geographically from north to south. The image includes the IMS logo, the date, and weather icons for each city. The image has a daily random gradient background.
4.  **Deliver Image:** The application can deliver the generated image via email using either SMTP or SendGrid.

## Project Structure

The project is organized into the following directory structure:

```
Automated-Daily-Forecast/
├── forecast_workflow.py      # Main orchestration script
├── download_forecast.py      # XML download & encoding
├── extract_forecast.py       # Data extraction
├── generate_forecast_image.py # Image generation
├── send_email.py             # SendGrid email delivery
├── send_email_smtp.py        # SMTP email delivery
├── utils.py                  # Shared utilities
├── archive/                  # Historical XML (14 days)
├── assets/                   # Logos, weather icons, and fonts
├── docs/                     # Project documentation
├── exploration/              # Test & development scripts
├── logs/                     # Automation logs
├── output/                   # Generated images
├── .github/                  # GitHub Actions workflows
├── requirements.txt          # Python dependencies
└── README.md                 # Project README
```

## Core Modules

The project is built around a set of core Python modules:

*   **`forecast_workflow.py`:** This is the main entry point of the application. It orchestrates the entire workflow by calling the other modules in the correct order. It also handles command-line arguments and logging.
*   **`download_forecast.py`:** This module is responsible for downloading the XML forecast data from the IMS website. It includes features like retry logic, timeout handling, and encoding conversion (from ISO-8859-8 to UTF-8). It also manages an archive of historical forecast data.
*   **`extract_forecast.py`:** This module parses the XML data and extracts the weather forecast for each of the 15 target cities. It then sorts the cities by latitude (from north to south) and validates the extracted data.
*   **`generate_forecast_image.py`:** This module uses the `Pillow` library to generate the final forecast image. It includes extensive configuration options for fonts, colors, and layout. It also handles the rendering of right-to-left (RTL) Hebrew text and generates a random gradient background for each image.
*   **`send_email.py`:** This module handles email delivery of the forecast image using the SendGrid API.
*   **`send_email_smtp.py`:** This module handles email delivery of the forecast image using a standard SMTP server.
*   **`utils.py`:** This module contains a collection of utility functions that are shared across the other modules. This includes functions for logging, date handling, file management, and data validation.

## Key Features

*   **Automated Workflow:** The entire process of downloading, processing, generating the forecast image, and sending it via email is fully automated using GitHub Actions.
*   **Robust Error Handling:** The application includes comprehensive error handling, including retry logic for network requests and fallback to archived data.
*   **Hebrew Language Support:** The application correctly handles Hebrew text, including right-to-left (RTL) rendering in the generated image.
*   **Configurable Design:** The visual design of the forecast image is highly configurable, with constants for fonts, colors, and layout defined at the top of the `generate_forecast_image.py` script.
*   **Dynamic Image Backgrounds:** The application generates a new random gradient background for the forecast image each day.
*   **Multiple Email Delivery Options:** The application supports email delivery via both SMTP and SendGrid.
*   **Modular Architecture:** The project is well-structured and modular, making it easy to understand, maintain, and extend.
*   **Dry-Run Mode:** A `--dry-run` option to simulate the entire workflow without making any changes to the file system or sending emails.
*   **Gradient Test Mode:** A `gradient-test` mode to generate a set of test images with different gradient backgrounds.

## Usage

### Prerequisites

*   Python 3.13+
*   An internet connection
*   SendGrid API key (if using the SendGrid email option)
*   SMTP server credentials (if using the SMTP email option)

### Installation

1.  Clone the repository.
2.  Install the required Python packages using pip:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

To run the complete workflow, execute the `forecast_workflow.py` script:

```bash
python forecast_workflow.py
```

This will download the latest forecast, extract the data, generate a new forecast image in the `output` directory, and send it via email.

You can also run the workflow in "dry-run" mode, which will simulate the process without creating or modifying any files:

```bash
python forecast_workflow.py --dry-run
```

To test the gradient generation, you can run the `test_gradients.py` script:

```bash
python test_gradients.py
```
