import { useContext, useEffect, useRef, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

// import styles from "./Matches.module.css";
import { API_URL } from "constants";
import SidebarPage from "pages/wrapper/SidebarPage";
import LoadingIndicator from "components/loading/LoadingIndicator";
import { EventContext } from "contexts/EventContext";
import { useIsFirstRender, usePrevious } from "utils/hooks";
import { capitalize, objectToParamsString, paramsStringToObject } from "utils";
import { Link } from "react-router-dom";
import TablePagination from "components/pagination/TablePagination";
import styles from "./TableSearchPage.module.css";
import Cookies from "universal-cookie";
//instantiating Cookies class by creating cookies object
const cookies = new Cookies();
export default function TableSearchPage({
  SidebarComponent,
  TableComponent,
  apiName,
  label,
}) {
  const { event, setEvent } = useContext(EventContext);
  const [filters, setFilters] = useState({});
  const [rows, setRows] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [alreadyChanged, setAlreadyChanged] = useState(false);
  const location = useLocation();
  const navigate = useNavigate();

  const [currentPage, setCurrentPage] = useState(1);
  const prevPage = usePrevious(currentPage);
  const [pageSize, setPageSize] = useState(10);
  const [totalCount, setTotalCount] = useState(0);

  const rootRef = useRef();
  const abortControllerRef = useRef(new AbortController());
  const pathnameRef = useRef(location.pathname);
  const keepLoading = useRef(false);
  const isFirstRender = useIsFirstRender();

  function fetchData({ scrollToTop = true } = {}) {
    // Abort previous request
    abortControllerRef.current.abort();
    abortControllerRef.current = new AbortController();
    // Prevent previous request from setting loading off when canceled
    if (isLoading) keepLoading.current = true;
    setIsLoading(true);
    console.log("location:",location)
    axios
      .get(`${API_URL}/${apiName}/${location.search}`, { headers:{
        "X-CSRFToken": cookies.get("csrftoken")
      },
      credentials: "same-origin",
      withCredentials:true,
        
        signal: abortControllerRef.current.signal,
      })
      .then((response) => {
        setRows(response.data.results);
        setTotalCount(response.data.count);
        setPageSize(response.data.page_size);
        setCurrentPage(response.data.current);
        if (scrollToTop) rootRef.current.scrollTo(0, 0);
      })
      .finally(() => {
        if (!keepLoading.current) {
          setIsLoading(false);
        }
        keepLoading.current = false;
      })
      .catch((error) => {
        if (axios.isCancel(error)) {
          // do nothing
        } else {
          throw error;
        }
      });
  }

  useEffect(() => {
    return () => {
      abortControllerRef.current.abort();
      setIsLoading(false);
    };
  }, []);

  useEffect(() => {
    if (!event || location.pathname !== pathnameRef.current) return;

    // Load filters from URL
    if (alreadyChanged) {
      setAlreadyChanged(false);
    } else {
      const params = paramsStringToObject(location.search);
      const { page: pageParam, ...filtersParam } = params;
      if ( pageParam === undefined) {
        params.page = pageParam ?? 1;
        navigate("?" + objectToParamsString(params), { replace: true });
        return;
      }
      
      setCurrentPage(pageParam);
      setFilters(filtersParam);
      setAlreadyChanged(true);
    }

    fetchData();
  }, [location]);

  useEffect(() => {
    if (!event || isFirstRender) return;
    if (alreadyChanged) {
      setAlreadyChanged(false);
    } else {
      const searchFilters = { event: event.id, ...filters, page: currentPage };
      console.log(currentPage, prevPage);
      if (currentPage !== 1 && prevPage === currentPage) {
        setCurrentPage(1);
        return;
      }
      navigate("?" + objectToParamsString(searchFilters));
      setAlreadyChanged(true);
    }
  }, [event, currentPage, filters]);

  const paginationEl = (
    <TablePagination
      current={currentPage}
      size={pageSize}
      count={totalCount}
      setCurrent={setCurrentPage}
      className={styles.pagination}
    />
  );

  return (
    <SidebarPage
      sidebar={<SidebarComponent filters={filters} setFilters={setFilters} />}
      rootRef={rootRef}
    >
      <h1 className={styles.title}>{capitalize(label)}</h1>
      <LoadingIndicator isLoading={isLoading} />
      <h4>{event?.name}</h4>

      <Link to="/dataLoad">
      <button type="button" class="btn btn-primary" >Cargar datos</button>
      </Link>
      

      {rows.length > 0 ? (
        <>
          {paginationEl}
          <TableComponent rows={rows} fetchData={fetchData} />
          {paginationEl}
        </>
      ) : (
        <p className={styles.infoText}>
          No se encontraron {label} con los criterios seleccionados
        </p>
      )}

      {event === undefined && (
        <p className={styles.infoText}>No se ha seleccionado un evento</p>
      )}
    </SidebarPage>
  );
}