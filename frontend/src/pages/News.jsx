export default function News() {
  return (
    <section class="my-2">
      <div class="d-flex row w-100 justify-content-center">
        <h2 class="h1-responsive font-weight-bold text-center my-5">
          Ultimas Noticias
        </h2>
        {/* {% if person.is_organizer or person.is_admin %} */}
        <a
          class="btn btn-danger btn-circle my-auto ml-5"
          data-toggle="modal"
          data-target=".new_news"
        >
          <i class="fas fa-plus"></i>
        </a>
        {/* {% endif %} */}
      </div>
      <div class="d-flex">
        <form class="w-100 d-flex" method="POST" id="category_filter">
          <div class="row w-100 justify-content-end mb-sm-2">
            <div class="col-sm-6 col-md-3 my-auto">
              <select class="form-control" name="category">
                <option value="all" selected>
                  Todas las categorias
                </option>
                {/* {% for category in categories %} */}
                <option value="{{ category.id }}" class="mb-2">
                  [CATEGORY]
                </option>
                {/* {% endfor %} */}
              </select>
            </div>
            <button
              class="btn btn-green ml-3 mr-4 my-auto"
              onclick="$('#category_filter').submit()"
            >
              Filtrar noticias
            </button>
          </div>
        </form>
      </div>
      {/* {% if news %} */}
      <div class="d-flex col-md-11 mx-auto">
        <table id="dt-select" class="table" cellspacing="0" width="100%">
          <thead style={{display: "none"}}>
            <tr>
              <th></th>
            </tr>
          </thead>
          <tbody>
            {/* {% for new in news %} */}
            <tr>
              <td>
                <div class="row">
                  <div class="col-lg-5">
                    <div class="view overlay rounded z-depth-2 mb-lg-0 mb-4">
                      <img
                        class="img-fluid"
                        src="{{ new.picture.url }}"
                        alt="{{ new.title }}"
                      />
                      <a>
                        <div class="mask rgba-white-slight"></div>
                      </a>
                    </div>
                  </div>
                  <div class="col-lg-7">
                    <a href="#!" class="{{ new.category.color }}-text category">
                      <h6 class="font-weight-bold mb-3">[ICO][CATEGORY]</h6>
                    </a>
                    <h3 class="font-weight-bold mb-3">
                      <strong>[TITLE]</strong>
                    </h3>
                    <p class="news_short">[SHORT_STORY]</p>
                    <p class="news_long d-none">[BODY]</p>
                    <p class="news_data">
                      by{" "}
                      <a>
                        <strong>[PUBLISHER]</strong>
                      </a>
                      , [DATE]
                    </p>
                    <a class="btn {{ new.category.btn_class }} btn-md open-modal">
                      Mas Información
                    </a>
                  </div>
                </div>
              </td>
            </tr>
            {/* {% endfor %} */}
          </tbody>
        </table>
      </div>
      {/* {% else %} */}
      <h3 class="h3-responsive font-weight-bold text-center my-5">
        No hay publicaciones para los valores seleccionados
      </h3>
      {/* {% endif %} */}
    </section>
  );
}
