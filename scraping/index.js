const extract = require("./extract");
const browserObject = require("./browser");
const fs = require("fs");

//Start the browser and create a browser instance
let browserInstance = browserObject.startBrowser();

const delay = (ms) => new Promise((res) => setTimeout(res, ms));

// Pass the browser instance to the scraper controller
async function scrapeAll() {
  const data = fs.readFileSync("./startup_link.txt", "utf8").split("\n");
  const preloadFile = fs.readFileSync("./preload.js", "utf8");

  const browser = await browserInstance;
  for (let link of data) {
    let page = await browser.newPage();
    // await page.evaluateOnNewDocument(preloadFile);
    await page.goto("https://www.crunchbase.com" + link);
    const searchResultSelector = "identifier-image img";
    await page.waitForSelector(searchResultSelector);

    const res = await page.evaluate(extract);

    console.log(res);
    await delay(3000);
  }
}

scrapeAll();
