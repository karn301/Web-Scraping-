let isExtensionActive = false;

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  if (message.action === "toggleExtension") {
    isExtensionActive = !isExtensionActive;
    // You can perform actions here when the extension is toggled on/off
    if (isExtensionActive) {
      // Extension is turned on, you can perform actions here
      alert("Amazon Auto Turn On Extension is active!");
    }
  }
});