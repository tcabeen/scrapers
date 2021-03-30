# Introduction

I've spent the last 6 years scraping data from websites, APIs, and even FTP sites. As I prepare for a transition to my next career, it occurs to me that my employer owns all those scripts. What they don't own is my knowledge, so I've created a repository to create meaningful scrapes with the intent of showing a variety of techniques that may benefit other developers down the road.

The code that I wrote for The Company is all proprietary, but what I've posted here is free to learn from, copy, or use outright.

# Code Notes

The code is all functional, and in most cases relatively few functions are used. This is a byproduct of working in a data operations group instead of a software development group. The structures of the teams and codebase are such that no two people are working in related files at any given time, so minimal change control is needed. Git is used more for version management and backups than it is for collaboration. We architect, write, test, and approve our own code. It's wild.

# Project Notes

I'll add some notes here to summarize the projects as I add them as well, with the goal of directing people to those that may be of greatest interest to them.

## Canadian Pacific Carloads scrape

This page has an XLSX file download link on it, but that link does not exist in the HTML source. The scrape creates POST requests to get the necessary information before calling the XLSX link directly and saving the file.

Features:

- JSON parsing
- HTTP POST requests
- Session management
- Saving binary data
