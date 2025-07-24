# Movie Data Search and Save

A simple web application for searching and saving movie data using the TMDb (The Movie Database) API.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This web application allows users to search for movies based on various criteria such as the number of movies, release year, genre, etc. The application uses the TMDb API to fetch movie data and saves the results in a CSV file. The user interface provides a simple form for input parameters and displays the search results.

## Features

- Search for movies based on criteria like number, release year, and genre.
- Save movie data to a CSV file.
- User-friendly web interface.
- Easy customization for additional features.

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python installed
- TMDb API Key (Get it from [TMDb](https://www.themoviedb.org/documentation/api))

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/esatarslan/agent_based_data_acq_tmdb.git
   ```
   ```
   cd movie-data-search
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Configure API Key:
   Obtain a TMDb API Key and update it in the config.py file:
   ```
   api_key = "your_tmdb_api_key"
   ```
## Usage
Run the application:

  ```bash
  python main.py
  ```
  Open your web browser and go to http://localhost:8080/ to access the application.

  Use the form to input search parameters and click "Search and Save" to fetch and save movie data.
## File Structure
main.py: Main application file.  
config.py: Configuration file for API key.  
templates/: HTML templates for the web interface.  
static/: Static files such as CSS styles.  

## License
This project is licensed under the [MIT License](/license.md).
