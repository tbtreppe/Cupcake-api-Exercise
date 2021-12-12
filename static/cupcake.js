const BASE_URL = "http://localhost:5000/api";

function getCupcakeHTML(cupcake) {
  return `<div data-cucpake-id={cupcake.id}> <li> ${cupcake.flavor} / ${cupcake.size} / ${cupcake.rating} <button class="delete-button"></button></li> <img class="Cupcake-img" src="${cupcake.image}" alt="(no image provided)"></div>`;
}

async function showCupcakes() {
  const response = await axios.get(`${BASE_URL}/cupcakes`);

  for (let cupcakeData of response.data.cupcakes) {
    let newCupcake = $(getCupcakeHTML(cupcakeData));
    $("#cupcake-list").append(newCupcake);
  }
}

$(".add-cupcake").click(addCupcake);
async function addCupcake() {
  await axios.post(`/api/cupcake`);
  $(this).parent().append();
}

$("new-cupcake-form").on("submit", async function (evt) {
  evt.preventDefault();

  let flavor = $("#form-flavor").val();
  let size = $("#form-size").val();
  let rating = $("#form-rating").val();
  let image = $("#form-image").val();

  const newCupcakeResponse = await axios.post(`${BASE_URL}/cupcakes`, {
    flavor,
    size,
    rating,
    image,
  });
  let newCupcake = $(getCupcakeHTML(newCupcakeResponse.data.cupcake));
  $("#cupcakes-list").append(newCupcake);
  $("#new-cupcake-form").trigger("reset");
});

$("#cupcake-list").on("click", ".delete-button", async function (evt) {
  evt.preventDefault();
  let $cupcake = $(evt.target).closest("div");
  let cupcakeId = $cupcake.attr("data-cupcake-ide");

  await axios.delete(`${BASE_URL}/cupcakes/${cupcakeId}`);
  $cupcake.remove();
});

$(showCupcakes);
