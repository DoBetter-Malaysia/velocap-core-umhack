async function extract(page) {
  const delay = (ms) => new Promise((res) => setTimeout(res, ms));

  const data = {
    image: "",
    name: "",
    homepage_url: "",
    country_name: "",
    category_list: "",
    founded_at: "",
    founders: "",
    status: "",
    funding_rounds: "",
    funding_total_usd: "",
    first_funding_at: "",
    last_funding_at: "",
  };

  const tabs = page.document.querySelectorAll("header nav .mat-tab-links a");

  let imageContainer =
    page.document.getElementsByTagName("identifier-image")[0];
  if (imageContainer != null) {
    data.image = imageContainer.querySelector("img").src;
  }

  data.name = page.document
    .getElementsByClassName("profile-name")[0]
    .innerHTML.trim();

  data.homepage_url = page.document.querySelector(
    "fields-card .icon_and_value li link-formatter a"
  )?.href;

  let geo = page.document.querySelectorAll(
    "fields-card .icon_and_value .ng-star-inserted identifier-multi-formatter span a"
  );

  if (geo.length > 0) {
    data.country_name = geo[geo.length - 1].innerHTML.trim();
  }

  let profiles = page.document.querySelectorAll(
    "profile-section .section-content ul.text_and_value li.ng-star-inserted"
  );

  let isIpo = false;

  for (let profile of profiles) {
    let innerText = profile.innerText;
    if (innerText.startsWith("Industries")) {
      let industries = profile.querySelector(
        "field-formatter chips-container"
      ).children;
      const res = [];
      for (let industry of industries) {
        res.push(industry.querySelector(".chip-text").innerHTML);
      }
      data.category_list = res.join("|");
    }

    if (innerText.startsWith("Founded Date")) {
      data.founded_at = profile
        .querySelector(
          ".component--field-formatter.field-type-date_precision.ng-star-inserted"
        )
        .innerHTML.trim();
    }

    if (innerText.startsWith("Founders")) {
      const founders = profile.querySelectorAll(
        "a.link-accent.ng-star-inserted"
      );
      const res = [];

      for (let founder of founders) {
        res.push(founder.innerHTML.trim());
      }
      data.founders = res.join("|");
    }

    if (innerText.startsWith("Operating Status")) {
      data.status = profile
        .querySelector(
          "span.component--field-formatter.field-type-enum.ng-star-inserted"
        )
        ?.innerText.trim();
    }

    if (innerText.startsWith("Last Funding Type")) {
      if (profile.querySelector("field-formatter").innerText.includes("IPO")) {
        isIpo = true;
      }
    }
  }

  if (data.status == "Closed") {
    if (page.document.querySelector("acquired_by" != null)) {
      data.status = "acquired";
    } else {
      data.status = "closed";
    }
  } else {
    if (isIpo) {
      data.status = "ipo";
    } else {
      data.status = "operating";
    }
  }

  tabs[1].click();

  // Financial
  await delay(2000);
  let highlights = page.document.querySelectorAll(
    ".onboarding-highlight-wrapper anchored-values div"
  );
  for (let highlight of highlights) {
    const label = highlight.querySelector("label-with-info")?.innerText ?? "";
    if (label.startsWith("Funding Rounds")) {
      data.funding_rounds = highlight.querySelector(
        "field-formatter span"
      ).innerText;
    } else if (label.startsWith("Total Funding Amount")) {
      data.funding_total_usd = highlight.querySelector(
        "field-formatter span"
      ).innerText;
      let fund = data.funding_total_usd;
      if (fund.startsWith("$")) {
        fund = fund.slice(1);
      }
      if (!/^\d$/.test(fund[fund.length - 1])) {
        let sign = fund[fund.length - 1];
        fund = fund.slice(0, fund.length - 1);
        fund = +fund;
        if (sign == "B") {
          fund *= 1_000_000_000;
        } else if (sign == "M") {
          fund *= 1_000_000;
        } else if (sign == "K") {
          fund *= 1_000;
        }
        data.funding_total_usd = fund;
      }
    }
  }

  for (let row of page.document.querySelectorAll("row-card")) {
    if (
      row
        .querySelector("h2.section-title")
        ?.innerText.startsWith("Funding Rounds")
    ) {
      let table = row.querySelectorAll("table tbody tr");
      if (table.length > 0) {
        data.last_funding_at = table[0]?.querySelector(
          ".ng-star-inserted field-formatter span.component--field-formatter.field-type-date.ng-star-inserted"
        ).innerText;
      }
      if (table.length > 1) {
        data.first_funding_at = table[table.length - 1]?.querySelector(
          ".ng-star-inserted field-formatter span.component--field-formatter.field-type-date.ng-star-inserted"
        ).innerText;
      }
    }
  }
  return data;
}

module.exports = extract;
