const fs = require("fs");
const path = require("path");
const studioPath = "/home/xyz/xyz-studio-front";
const outputPath = "/home/xyz/studio_i18n.html";

//要遍历的文件夹所在的路径
let translationDict = {};
let dataForHtml = [];

main();

function main() {
  let filePath = path.join(studioPath, "src/app");
  genTranslationDict(filePath);
  console.log("================ genTranslationDict done ================");
  convertToJson();
  console.log("================ convertToJson done ================");
  genHtmlDynamic();
  console.log("================ genHtmlDynamic done ================");
}

function genTranslationDict(filePath) {
  //根据文件路径读取文件，返回文件列表
  const files = fs.readdirSync(filePath);
  //遍历读取到的文件列表
  files.forEach(function (filename) {
    //获取当前文件的绝对路径
    var filedir = path.join(filePath, filename);
    //根据文件路径获取文件信息，返回一个fs.Stats对象
    const stats = fs.statSync(filedir);
    var isFile = stats.isFile(); //是文件
    var isDir = stats.isDirectory(); //是文件夹
    if (isFile && isFileValid(filedir)) {
      regFile(filedir, "overallPage.nextItemTip");
    }
    if (isDir) {
      genTranslationDict(filedir); //递归，如果是文件夹，就继续遍历该文件夹下面的文件
    }
  });
}

function convertToJson() {
  let jsonPathCN = path.join(studioPath, "src/assets/i18n/zh_cn.json");
  let rawDataCN = fs.readFileSync(jsonPathCN);
  let jsonDataCN = JSON.parse(rawDataCN.toString());

  let jsonPathEN = path.join(studioPath, "src/assets/i18n/en.json");
  let rawDataEN = fs.readFileSync(jsonPathEN);
  let jsonDataEN = JSON.parse(rawDataEN.toString());

  // 构建rawDataCN的行数map
  const lines = rawDataCN.toString().split('\n')
  let level1 = ''
  let level2 = ''

  const regLevel1 = new RegExp('\\"(\\w+?)\\"\\s*?\\:\\s*?\\{')
  const regLevel2 = new RegExp('\\"(\\w+?)\\"\\s*?\\:\\s*?\\"')
  const langLineNumberDict = {}

  lines.forEach((line, lineNumber) => {
    const result1 = regLevel1.exec(line)
    if (result1) {
      level1 = RegExp.$1
    }
    const result2 = regLevel2.exec(line)
    if (result2) {
      level2 = RegExp.$1
      const key = level1 + '.' + level2
      langLineNumberDict[key] = lineNumber + 1
    }
  })

  Object.keys(jsonDataCN).forEach((key1) => {
    Object.keys(jsonDataCN[key1]).forEach((key2, number) => {
      const searchParam = key1 + "." + key2;
      const cn = jsonDataCN[key1][key2];
      let en = "";
      try {
        en = jsonDataEN[key1][key2];
      } catch (e) {}
      const refer =
        searchParam in translationDict ? translationDict[searchParam] : {};
      const enPath = `${jsonPathEN}:${searchParam in langLineNumberDict?langLineNumberDict[searchParam]:1}`
      const cnPath = `${jsonPathCN}:${searchParam in langLineNumberDict?langLineNumberDict[searchParam]:1}`
      dataForHtml.push({
        name: searchParam,
        cn: cn,
        en: en,
        enPathWithLine: enPath,
        cnPathWithLine: cnPath,
        refer: refer,
      });
    });
  });
}

function isFileValid(filePath) {
  const ext = path.extname(filePath);
  if (![".html", ".ts"].includes(ext)) {
    return false;
  }

  const filePathSplit = filePath.split(".");
  if (ext === ".ts" && filePathSplit[filePathSplit.length - 2] === "spec") {
    return false;
  }

  return true;
}

/**
 * 通过正则匹配所有文件，找出xxx.xxx所在的行
 * @param filePath
 * @param param
 */
function regFile(filePath) {
  const ext = path.extname(filePath);
  const data = fs.readFileSync(filePath).toString();
  if (ext === ".ts" || ext === ".html") {
    let lines = data.split("\n");
    let reg2 = new RegExp(`(\\'\\w+?\\.\\w+?\\'|\\"\\w+?\\.\\w+?\\")`, "g");
    lines.forEach((line, lineBNumber) => {
      while ((result = reg2.exec(line))) {
        let keyName = RegExp.$1.replaceAll('\'', '').replaceAll('\"', '');
        if (!(keyName in translationDict)) {
          translationDict[keyName] = [];
        }
        translationDict[keyName].push({
          filePath: filePath,
          number: lineBNumber + 1,
        });
      }
    });
  }
}

function genHtmlDynamic() {
  const template = fs.readFileSync("./template.html").toString();
  const reg = new RegExp("{%\\s*(\\w+)\\s*%}");
  const data = dataForHtml;
  const newTemplate = template.replace(reg, JSON.stringify(data));
  fs.writeFile(outputPath, newTemplate, (err) => {
    if (err) {
      console.log(err);
      return;
    }
  });
}
