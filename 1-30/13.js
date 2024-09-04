const now = new Date();
const jstString = new Date(now.getTime() + 9 * 60 * 60 * 1000)
  .toISOString()
  .replace("Z", "+09:00");

console.log("console.log('=======================================')");
console.log("console.log('  #   ')");
console.log("console.log(' ##   ')");
console.log("console.log('  #   ')");
console.log("console.log('  #   ')");
console.log("console.log(' ###  ')");
console.log(
  "console.log(`===001==${" + jstString + "}== valName: ${valName}`)"
);
console.log("");
console.log("console.log('=======================================')");
console.log("console.log('  ##  ')");
console.log("console.log(' #  # ')");
console.log("console.log('   #  ')");
console.log("console.log('  #   ')");
console.log("console.log(' #### ')");
console.log(
  "console.log(`===002==${" + jstString + "}== valName: ${valName}`)"
);
console.log("");
console.log("console.log('=======================================')");
console.log("console.log(' ###  ')");
console.log("console.log('   #  ')");
console.log("console.log('  ##  ')");
console.log("console.log('   #  ')");
console.log("console.log(' ###  ')");
console.log(
  "console.log(`===003==${" + jstString + "}== valName: ${valName}`)"
);
