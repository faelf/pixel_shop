// Pure JavaScript for Quantity Logic (No jQuery needed here)
document.addEventListener("DOMContentLoaded", function () {
  function handleEnableDisable(itemId) {
    const input = document.querySelector(`#id_qty_${itemId}`);
    if (!input) return;

    const currentValue = parseInt(input.value);
    const inputGroup = input.closest(".input-group");
    if (!inputGroup) return;

    const decrementBtn = inputGroup.querySelector(".qty_minus");
    const incrementBtn = inputGroup.querySelector(".qty_plus");

    // Use the min/max attributes on the input for strict limits
    const max = parseInt(input.getAttribute("max")) || 99;
    const min = parseInt(input.getAttribute("min")) || 1;

    if (decrementBtn) decrementBtn.disabled = currentValue <= min;
    if (incrementBtn) incrementBtn.disabled = currentValue >= max;
  }

  function updateForm(element) {
    // Use the closest() method to find the form and submit it
    element.closest("form").submit();
  }

  function checkAndSubmit(element) {
    // Only auto-submit forms with the specific class
    if (element.closest("form").classList.contains("js-update-form")) {
      updateForm(element);
    }
  }

  // Initialize all quantity inputs on page load
  document
    .querySelectorAll(".form-control[name='quantity']")
    .forEach((input) => {
      const itemId = input.dataset.itemId;
      handleEnableDisable(itemId);

      // Listener for manual input change
      input.addEventListener("change", (e) => {
        handleEnableDisable(itemId);
        checkAndSubmit(e.target);
      });
    });

  // Increment quantity (+ button click)
  document.querySelectorAll(".qty_plus").forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      const input = button
        .closest(".input-group")
        .querySelector("input[name='quantity']");

      input.value = parseInt(input.value) + 1;

      handleEnableDisable(button.dataset.itemId);
      checkAndSubmit(button);
    });
  });

  // Decrement quantity (- button click)
  document.querySelectorAll(".qty_minus").forEach((button) => {
    button.addEventListener("click", (e) => {
      e.preventDefault();
      const input = button
        .closest(".input-group")
        .querySelector("input[name='quantity']");

      input.value = parseInt(input.value) - 1;

      handleEnableDisable(button.dataset.itemId);
      checkAndSubmit(button);
    });
  });

  $(".remove-item").click(function (e) {
    e.preventDefault();
    var csrfToken = "{{ csrf_token }}";
    var itemId = $(this).attr("id").split("remove_")[1];
    var size = $(this).data("size");
    var url = `/trolley/remove/${itemId}`;
    var data = { csrfmiddlewaretoken: csrfToken, size: size };

    $.post(url, data)
      .done(function () {
        location.reload();
      })
      .fail(function (jqXHR, textStatus, errorThrown) {
        console.error("Remove failed:", textStatus, errorThrown);
      });
  });
});
