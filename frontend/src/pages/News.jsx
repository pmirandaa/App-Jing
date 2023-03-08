import {
  Button,
  Modal
} from "react-bootstrap";
import { useEffect, useState, useContext } from "react";
import AuthContext from "contexts/UserContext";

export default function News() {
  const [addNewsModal, setAddNewsModal] = useState(false);
  const { user } = useContext(AuthContext);
  const { permissions } = useContext(AuthContext);

  const toggleAddNewsModal = () => setAddNewsModal(!addNewsModal);
   console.log(user);
   console.log(permissions);

  return (
    <div>
      <section class="my-2">
        <div class="d-flex row w-100 justify-content-center">
          <h2 class="h1-responsive font-weight-bold text-center my-5">
            Ultimas Noticias
          </h2>
          {/* {% if person.is_organizer or person.is_admin %} */}
          <Button
            onClick={toggleAddNewsModal}
            class="btn btn-danger btn-circle my-auto ml-5"
          >
            +
          </Button>
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
                onClick="$('#category_filter').submit()"
              >
                Filtrar noticias
              </button>
            </div>
          </form>
        </div>
        {/* {% if news %} */}
        <div class="d-flex col-md-11 mx-auto">
          <table id="dt-select" class="table" cellspacing="0" width="100%">
            <thead style={{ display: "none" }}>
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
                      <a
                        href="#!"
                        class="{{ new.category.color }}-text category"
                      >
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
      <Modal isOpen={addNewsModal} toggle={setAddNewsModal} size="xl">
        <div class="modal-body">
          <button
            type="button"
            class="close"
            data-dismiss="modal"
            aria-label="Close"
          >
            <span aria-hidden="true">&times;</span>
          </button>
          <form
            method="POST"
            action="{% url 'news:create' %}"
            enctype="multipart/form-data"
            id="news_form"
          >
            <div class="row mt-4">
              <div class="col-lg-5">
                <div
                  class="view overlay rounded z-depth-2 mb-lg-0 mb-4"
                  style={{ minHeight: "300px" }}
                  id="news_img"
                >
                  <input
                    type="file"
                    class="form-control"
                    style={{ marginTop: "120px", paddingBottom: "37px" }}
                    id="news_img_input"
                    name="image"
                  />
                </div>
              </div>
              <div class="col-lg-7">
                <select class="form-control mb-3" name="category">
                  <option value="" disabled selected>
                    Elijá categoría
                  </option>
                  {/* {% for category in categories %} */}
                  <option value="{{ category.id }}" class="mb-2">
                    [CATEGORY]
                  </option>
                  {/* {% endfor %} */}
                </select>
                <div class="md-form mb-4">
                  <input
                    type="text"
                    id="news_title"
                    name="title"
                    class="form-control validate"
                  />
                  <label
                    data-error="wrong"
                    data-success="right"
                    for="news_title"
                  >
                    Titulo de la noticia
                  </label>
                </div>
                <div class="md-form mb-4">
                  <textarea
                    id="news_resume"
                    name="resume"
                    class="md-textarea form-control"
                    rows="3"
                  ></textarea>
                  <label
                    data-error="wrong"
                    data-success="right"
                    for="news_resume"
                  >
                    Bajada de la noticia (Texto corto)
                  </label>
                </div>
              </div>
            </div>
            <hr class="my-5" />
            <div class="md-form mb-4">
              <textarea
                id="news_body"
                name="body"
                class="md-textarea form-control"
                rows="5"
              ></textarea>
              <label data-error="wrong" data-success="right" for="news_resume">
                Cuerpo de la noticia (Texto largo)
              </label>
            </div>
            <div class="row justify-content-end">
              <button
                class="btn btn-success btn-md mr-3"
                onclick="$('#news_form').submit();"
              >
                Agregar Noticia
              </button>
            </div>
          </form>
        </div>
      </Modal>
    </div>
  );
}
