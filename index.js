const { documentToHtmlString } = require("@contentful/rich-text-html-renderer");
const axios = require("axios");
const fs = require("fs");
const url =
  "https://cdn.contentful.com/spaces/hsqegln674a1/environments/master/entries?access_token=bL7YuL04zCyiOLlVheOZ7duN7awl-WFir8o7PTIUDfI&content_type=startup&locale=ar";
axios.get(url).then((response) => {
  let data = [];
  response.data.items.map((item) => {
    data.push(item.fields);
  });
  let newData = data.map((item) => ({
    ...item,
    description: documentToHtmlString(item.description),
  }));
  let byOrder = newData.slice(0);
  byOrder.sort(function (a, b) {
    return a.order - b.order;
  });
  fs.writeFile("data.json", JSON.stringify(byOrder), "utf8", () => {});
});
