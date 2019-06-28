function UnityProgress(gameInstance, progress) {
  if (!gameInstance.Module)
    return;
  if (!gameInstance.logo) {
    gameInstance.logo = document.createElement("div");
    gameInstance.logo.className = "logo " + gameInstance.Module.splashScreenStyle;
    gameInstance.container.appendChild(gameInstance.logo);
  }
  if (!gameInstance.progress) {
    gameInstance.progress = document.createElement("div");
    gameInstance.progress.className = "progress " + gameInstance.Module.splashScreenStyle;
    gameInstance.progress.empty = document.createElement("div");
    gameInstance.progress.empty.className = "empty";
    gameInstance.progress.appendChild(gameInstance.progress.empty);
    gameInstance.progress.full = document.createElement("div");
    gameInstance.progress.full.className = "full";
    gameInstance.progress.appendChild(gameInstance.progress.full);
    gameInstance.container.appendChild(gameInstance.progress);
  }
  gameInstance.progress.full.style.width = (100 * progress) + "%";
  gameInstance.progress.empty.style.width = (100 * (1 - progress)) + "%";
  if (progress == 1)
    gameInstance.logo.style.display = gameInstance.progress.style.display = "none";

  setTimeout(function () {
    initUnity();
  }, 2500);


 


  function initUnity() {
    countMax = document.getElementById("fwTotal").getAttribute("value");
    console.log(countMax);

    var i = 0;
    while (i <= fwCategories.length - 1) {
      if (document.getElementById("fwType_" + fwCategories[i])) {
        for (v = 0; v <= (document.getElementById("fwCount_" + fwCategories[i]).getAttribute("value")); v++) {
          console.log("%*%*%%*%*%*%**%*%*%*%*%%*")
          console.log("fwType_" + fwCategories[i])
          gameInstance.SendMessage("FireworkSpawner", "loadSequence", ("fwType_" + fwCategories[i]));
        }
      }
      i++;
    }
    gameInstance.SendMessage("FireworkSpawner", "finishSequence", 1);
  }

}