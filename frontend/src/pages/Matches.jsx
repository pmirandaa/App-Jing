import MatchesSidebar from "components/sidebar/MatchesSidebar";
// import styles from "./Matches.module.css";
import MatchesTable from "components/table/MatchesTable";
import TableSearchPage from "./wrapper/TableSearchPage";

export default function Matches() {
  return (
    <TableSearchPage
      SidebarComponent={MatchesSidebar}
      TableComponent={MatchesTable}
      apiUrl="/api/matches/"
      label="partidos"
    />
  );
}
