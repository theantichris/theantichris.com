const blockcodes = document.querySelectorAll(".chroma code[data-lang]");

for (const bc of blockcodes) {
  const parent = bc.parentElement;
  const content = bc.innerText;

  // Code title
  const title = document.createElement("div");
  const lang = bc.dataset.lang;
  title.classList.add("code-title");
  title.innerText = lang;

  // Copy to clipboard
  if (navigator.clipboard !== undefined) {
    const cpbutton = document.createElement("button");
    cpbutton.classList.add("copy-button");
    cpbutton.innerText = "Copy";

    cpbutton.addEventListener("click", async () => {
      try {
        await navigator.clipboard.writeText(content);
      } catch {
        cpbutton.innerText = "Copy failed";
        return;
      }

      cpbutton.innerText = "Copied";
      setTimeout(() => {
        cpbutton.innerText = "Copy";
      }, 1000);
    });

    title.append(cpbutton);
  }

  parent.closest(".highlight").prepend(title);
}
