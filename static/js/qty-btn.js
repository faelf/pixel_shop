document.addEventListener("DOMContentLoaded", function () {
  // Disable +/- buttons outside 1-99 range
  function handleEnableDisable(itemId) {
    const input = document.querySelector(`#id_qty_${itemId}`);
    const currentValue = parseInt(input.value);

    const decrementBtn = input
      .closest(".input-group")
      .querySelector(".qty_minus");
    const incrementBtn = input
      .closest(".input-group")
      .querySelector(".qty_plus");

    decrementBtn.disabled = currentValue < 2;
    incrementBtn.disabled = currentValue > 98;
  }

  // Initialise all quantity inputs on page load
  document
    .querySelectorAll(".form-control[name='quantity']")
    .forEach((input) => {
      const itemId = input.dataset.itemId;
      handleEnableDisable(itemId);

      // Add change event listener
      input.addEventListener("change", () => {
        handleEnableDisable(itemId);
      });
    });

  // Increment quantity
  document.querySelectorAll(".qty_plus").forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      const input = button
        .closest(".input-group")
        .querySelector("input[name='quantity']");
      input.value = parseInt(input.value) + 1;
      handleEnableDisable(button.dataset.itemId);
    });
  });

  // Decrement quantity
  document.querySelectorAll(".qty_minus").forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      const input = button
        .closest(".input-group")
        .querySelector("input[name='quantity']");
      input.value = parseInt(input.value) - 1;
      handleEnableDisable(button.dataset.itemId);
    });
  });
});
