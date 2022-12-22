import MatchesSidebar from "pages/Matches/MatchesSidebar";
import MatchesTable from "pages/Matches/MatchesTable";
import TableSearchPage from "../wrapper/TableSearchPage";

export default function Matches() {
  return (
    <TableSearchPage
      SidebarComponent={MatchesSidebar}
      TableComponent={MatchesTable}
      apiName="matches"
      label="partidos"
    />
  );
}
