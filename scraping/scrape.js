const res = [];
const companies = [];

let input = document.getElementById("mat-input-0");

const after2sec = () => {
  try {
    let res = document.getElementsByTagName("search-results-section")[0];
    res.querySelector("mat-card a").href;
  } catch {
    after2sec();
  }
};

const delay = (ms) => new Promise((res) => setTimeout(res, ms));

async function scrape() {
  for (let c of companies) {
    input.value = c;
    input.dispatchEvent(new Event("input", { bubbles: true }));
    await delay(2000);
    after2sec();
  }
}

scrape();
console.log(res);
