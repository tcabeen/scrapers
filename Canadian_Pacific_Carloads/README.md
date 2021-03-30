# Canadian Pacific Carloads Scraper

This script simply scrapes the CP-Weekly-RTMs-and-Carloads.xlsx file from the page.

Requirements:

- Python 3.8
- requests library
- json library

## The Challenge

The button to download this file does not exist in the HTML. It is dynamically generated in Javascript.

## The Solution

On your home computer, you can just write a quick Selenium scrape and be done. In a non-containerized production environment, Selenium is a less ideal option due to its resource consumption. Too many Selenium scrapes, like too many open browser tabs, will quickly overwhelm a system.

Instead, we are going to study the page and follow the process the HTML uses to procure the link we need. Then we can download the XLSX with a simple GET request.

## Examining the Site

Quite a few steps in this process, but each is pretty straightforward:

First, we're going to get to some more information:

1. Load up [Canadian Pacific Key Metrics page](https://investor.cpr.ca/key-metrics/default.aspx)
2. Next open your browser's Inspector and select the Network tab
3. Reload the page to record what happens
4. At this point, you can stop recording, but it's not a terribly busy page, so your choice
5. In the filter bar, select XHR to hide all the JS and media calls, and so forth
6. You'll see two calls repeated several times, GetContentAssetYearList, and GetContentAssetList; let's learn more about them
7. Click on one of the GetContentAssetYearList entries, and a new pane will open

Understanding this pane takes a little time, but let's go through key sections.

- Headers / General: Tells us whether it was a GET or POST request and the URL
- Headers / Response Headers: Lots of interesting content, but nothing we need today
- Headers / Request Payload: This is what we'll need to send with the POST reqeust!
- Response: What we get back from the POST request!

We want to check the Response first for each of these, but at this time, we don't even know if or which of these we need. So let's move on to the GetContentAssetList calls.

## Finding Our Link

Leaving the Response tab open, click through the GetContentAssetList calls. We're looking for a response that includes our download link, but there are multiple "Download file" responses, so check the URL for the target filename as well.

Once you've found the correct call, return to the Headers tab, and copy the Request URL and Payload to your notes. In your browser's inspector, you may first need to click "view source" next to the Request Payload heading.

> https://investor.cpr.ca/Services/ContentAssetService.svc/GetContentAssetList
>
> {"serviceDto":{"ViewType":"2","ViewDate":"","RevisionNumber":"1","LanguageId":"1","Signature":"","ItemCount":1,"StartIndex":0,"TagList":["railcar"],"IncludeTags":true},"assetType":"Weekly Metrics - Download","year":2017}

## Backtracking for More Information

In the payload, you can see there's a year at the end, but we don't have enough information to programmatically create it. Is it current year - 4? But wait, let's revisit the GetContentAssetYearList calls!

Looking through the responses, there are requests that return a single year. Let's get the URL and Payload for one of those as well.

> https://investor.cpr.ca/Services/ContentAssetService.svc/GetContentAssetYearList
>
> {"serviceDto":{"ViewType":"2","ViewDate":"","RevisionNumber":"1","LanguageId":"1","Signature":"","TagList":["time"]},"assetType":"Weekly Metrics - Download"}

And we discover from the request payload that this call is specifically for the Weekly Metrics - Download, like the last. Fantastic.

## Writing the Scrape

With our research done, the scrape itself is going to be absolute cake.

1. GET main URL
2. Construct first POST
3. Parse results to get that year
4. Construct second POST
5. Parse results to get that URL
6. GET the file link
7. Save the file

The rest is just error handling.
