function wordBlanks(myNoun, myAdjective, myVerb, myAdverb) {
  return (
    "The " +
    myAdjective +
    " " +
    myNoun +
    " " +
    myVerb +
    " to the store " +
    myAdverb
  );
}
console.log("wordBlanks:", wordBlanks("cat", "black", "house", "quickly"));

var testObj = {
  hat: "ballcap",
  shirt: "jersey",
};
console.log(testObj.hat);
// console.log(testObj.hasOwnProperty("hat"));
// console.log(testObj.hasOwnProperty("hattt"));

const magic = () => new Date(); // an anonymous function
console.log("magic:", magic());

const myConcat = (arr1, arr2) => arr1.concat(arr2);
console.log("myConcat:", myConcat([1, 2], [3, 4]));

const squareOfPosInts = (arr) =>
  arr.filter((x) => Number.isInteger(x) && x > 0).map((x) => x ** 2);
console.log("squareOfPosInts:", squareOfPosInts([-1, 0, 1, 2, 3]));
