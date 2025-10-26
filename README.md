# Overview

As a cyber security major, I wanted to deepen my understanding of cloud-based application development and to learn how to integrate python code with the cloud to build a practical application that solves a real-world problem.

This program is a fitness tracker that allows users to input thier excerize data, including metrics such as calories burned and time (minutes) during given activity. Users are also able to register a new account and login to an existing account. All of this data is stored within the cloud database to display to the user thier excersize history depending on the account credentials.

{Provide a link to your YouTube demonstration. It should be a 4-5 minute demo of the software running, a walkthrough of the code, and a view of the cloud database.}

[Software Demo Video](https://youtu.be/ufh9LxLciWQ)

# Cloud Database

I'm using Google Firebase Firestore, a flexible, scalable NoSQL cloud database. Firestore stores data in collections containing documents, with each document containing key-value pairs. In the activities collection each document represents a single workout activity. Fields: user_id, activity_type, duration_minutes, calories_burned and date.

# Development Environment

Visual Studio Code - Primary code editor
Firebase Console - Web interface for managing the Firestore database and viewing data
Git - Version control
Windows Terminal - Command-line interface for running the application

# Future Work

- Password Authentication
- Data Visualization

- Export Functionality

