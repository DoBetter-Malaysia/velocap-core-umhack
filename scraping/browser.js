const puppeteer = require("puppeteer");

const args = [
  "--no-sandbox",
  "--disable-setuid-sandbox",
  "--disable-infobars",
  "--window-position=0,0",
];

const options = {
  args,
  headless: true,
  ignoreHTTPSErrors: true,
  userDataDir: "./tmp",
};

async function startBrowser() {
  let browser;
  try {
    console.log("Opening the browser......");
    browser = await puppeteer.launch({
      headless: false,
      args,
      ignoreHTTPSErrors: true,
    });
  } catch (err) {
    console.log("Could not create a browser instance => : ", err);
  }
  return browser;
}

module.exports = {
  startBrowser,
};
