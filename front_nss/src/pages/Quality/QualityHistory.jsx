import React, { useState } from "react";
import {
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Checkbox,
  TableSortLabel,
  TablePagination,
  Button,
} from "@mui/material";

const data = [
  { id: 673, product: "ОСАГО", status: "не пройдена", date: "10.12.2024 12:46:54" },
  { id: 672, product: "Страхование жизни", status: "не пройдена", date: "10.12.2024 11:56:01" },
  { id: 671, product: "ОСАГО", status: "не пройдена", date: "09.12.2024 8:12:28" },
  { id: 670, product: "Страхование жизни", status: "пройдена", date: "08.12.2024 05:46:20" },
  { id: 669, product: "ОСАГО", status: "пройдена", date: "07.12.2024 23:32:10" },
  { id: 668, product: "Страхование жизни", status: "не пройдена", date: "07.12.2024 15:57:13" },
  { id: 667, product: "Страхование жизни", status: "пройдена", date: "07.12.2024 12:46:54" },
  { id: 666, product: "ОСАГО", status: "пройдена", date: "06.12.2024 09:04:01" },
  { id: 665, product: "ОСАГО", status: "не пройдена", date: "06.12.2024 07:07:07" },
  { id: 664, product: "Страхование жизни", status: "пройдена", date: "06.12.2024 06:06:00" },
];

const ListQuality = () => {
  const [selected, setSelected] = useState([]);
  const [order, setOrder] = useState("asc");
  const [orderBy, setOrderBy] = useState("id");
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);

  const handleSort = (property) => {
    const isAscending = orderBy === property && order === "asc";
    setOrder(isAscending ? "desc" : "asc");
    setOrderBy(property);
  };

  const handleSelectAllClick = (event) => {
    if (event.target.checked) {
      const newSelected = data.map((row) => row.id);
      setSelected(newSelected);
      return;
    }
    setSelected([]);
  };

  const handleClick = (id) => {
    const selectedIndex = selected.indexOf(id);
    let newSelected = [];

    if (selectedIndex === -1) {
      newSelected = newSelected.concat(selected, id);
    } else if (selectedIndex === 0) {
      newSelected = newSelected.concat(selected.slice(1));
    } else if (selectedIndex === selected.length - 1) {
      newSelected = newSelected.concat(selected.slice(0, -1));
    } else if (selectedIndex > 0) {
      newSelected = newSelected.concat(
        selected.slice(0, selectedIndex),
        selected.slice(selectedIndex + 1)
      );
    }

    setSelected(newSelected);
  };

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const isSelected = (id) => selected.indexOf(id) !== -1;

  const sortedData = [...data].sort((a, b) => {
    if (order === "asc") {
      return a[orderBy] > b[orderBy] ? 1 : -1;
    }
    return a[orderBy] < b[orderBy] ? 1 : -1;
  });

  const paginatedData = sortedData.slice(
    page * rowsPerPage,
    page * rowsPerPage + rowsPerPage
  );

  return (
    <Box p={3} bgcolor="#1E1E2E" color="white">
      <Box display="flex" justifyContent="space-between" mb={2}>
        <span>Выбрано: {selected.length}</span>
        <Button variant="contained" color="secondary" onClick={() => setSelected([])}>
          Снять выделение
        </Button>
      </Box>
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell padding="checkbox">
                <Checkbox
                  indeterminate={selected.length > 0 && selected.length < data.length}
                  checked={selected.length === data.length}
                  onChange={handleSelectAllClick}
                />
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderBy === "id"}
                  direction={order}
                  onClick={() => handleSort("id")}
                >
                  № проверки
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderBy === "product"}
                  direction={order}
                  onClick={() => handleSort("product")}
                >
                  Вид продукта
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderBy === "status"}
                  direction={order}
                  onClick={() => handleSort("status")}
                >
                  Статус проверки
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={orderBy === "date"}
                  direction={order}
                  onClick={() => handleSort("date")}
                >
                  Дата
                </TableSortLabel>
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {paginatedData.map((row) => {
              const isItemSelected = isSelected(row.id);
              return (
                <TableRow
                  key={row.id}
                  onClick={() => handleClick(row.id)}
                  role="checkbox"
                  selected={isItemSelected}
                  hover
                >
                  <TableCell padding="checkbox">
                    <Checkbox checked={isItemSelected} />
                  </TableCell>
                  <TableCell>{row.id}</TableCell>
                  <TableCell>{row.product}</TableCell>
                  <TableCell>{row.status}</TableCell>
                  <TableCell>{row.date}</TableCell>
                </TableRow>
              );
            })}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[5, 10, 15]}
        component="div"
        count={data.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
      />
    </Box>
  );
};

export default ListQuality;
