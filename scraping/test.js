const res = [];
async function doAutomatedStuff(links) {
  //Use 'async' to make use of 'await' later
  for (const link of links) {
    let page = window.open(
      "https://www.crunchbase.com" + link,
      "",
      "location=no, toolbar=0, width=600, height=600"
    ); //Must be executed from the same website and pop-ups are allowed
    page.onload = async function (event) {
      res = await extract(page);
      page.close();
    };
    await new Promise((r) => setTimeout(r, 3000)); //Wait and block (delay) for a reasonable amount of time before proceeding to the next link
  }
}

doAutomatedStuff(pages); //Execute
