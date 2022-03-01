s = `
this.commonService.translateAsync([
    'artifactReg.trainLabel1',
    'artifactReg.trainLabel2',
  ]).subscribe(r => {
    this.trainParamsList[0].label = r['artifactReg.trainLabel1'];
    this.trainParamsList[1].label = r['artifactReg.trainLabel2'];
  });
}
this.commonService.translateAsync(['motionStg.inTip1', 'motionStg.inTip2', 'motionStg.inTip3', 'motionStg.inTip4']).subscribe(r => {
    this.i18n = {
      tip1: r['motionStg.inTip1'],
      tip2: r['motionStg.inTip2'],
      tip3: r['motionStg.inTip3'],
      tip4: r['motionStg.inTip4'],
    };
  });

this.overlayService.setSwitcherOn(this.commService.translate('cameraSetup.refreshing'));
`;
let translationDict = {}
function regFile() {
    let filePath = ''
    const data = s;
    let ext = '.ts'
    let reg;
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
    } else {
      reg = new RegExp(`{{\\s*('.*?'|".*?")\\s*\\|\\s*translate`, "g");
      let lines = data.split("\n");
      lines.forEach((line, lineBNumber) => {
        while ((result = reg.exec(line))) {
          const keyName = RegExp.$1.replaceAll('"', "").replaceAll("'", "");
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
    console.log(translationDict)
  }
  regFile()