import React, { useState, useEffect } from "react";
import {
  Box,
  Grid,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TablePagination,
  Paper,
  TextField,
} from "@mui/material";
import { DatePicker } from "@mui/x-date-pickers/DatePicker";
import { LocalizationProvider } from "@mui/x-date-pickers";
import { AdapterDateFns } from "@mui/x-date-pickers/AdapterDateFns";
import Header from "../../components/Header";
import api from "../../utils/api";

const DataMart = () => {
  const [filters, setFilters] = useState({
    product: "", // Показывает все продукты, если пустой
    model: "", // Показывает все модели, если пустой
    insuranceCase: "", // Показывает все страховые случаи, если пустой
    features: [], // Показывает все фичи, если пустой
  });

  const [data, setData] = useState([]); // Данные для таблицы
  const [page, setPage] = useState(0); // Текущая страница
  const [rowsPerPage, setRowsPerPage] = useState(10); // Количество строк на странице
  const [startDate, setStartDate] = useState(null); // Дата начала
  const [endDate, setEndDate] = useState(null); // Дата окончания
  const [loading, setLoading] = useState(false); // Индикатор загрузки

  const handleFilterChange = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value }));
  };

  const handlePageChange = (event, newPage) => {
    setPage(newPage);
  };

  const handleRowsPerPageChange = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const fetchData = async () => {
    setLoading(true);
    try {
      const response = await api.post("/dwh/", {
        "product_type": "string",
        "model_name": "string",
        "is_insurance_case": true,
        "feature_name": "string",
        "start_date": "2025-01-16",
        "end_date": "2025-01-16"
      });
      setData(response.data);
    } catch (error) {
      console.error("Ошибка при загрузке данных:", error);
    } finally {
      setLoading(false);
    }
  };

  // Запрос данных при монтировании страницы
  useEffect(() => {
    fetchData();
  }, []);

  // Обновление данных при изменении фильтров, даты, страницы или количества строк
  useEffect(() => {
    fetchData();
  }, [filters, startDate, endDate, page, rowsPerPage]);

  const columns = [
    "Продукт",
    "ID запроса",
    "ID категории",
    "Дата открытия",
    "Дата закрытия",
    "Модель",
    "Название фичи",
    "Значение фичи",
    "Скор балл",
    "Страховой случай",
  ];

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
      <Header title="Витрина данных" />

      <Box p={3}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth>
              <InputLabel>Продукт</InputLabel>
              <Select
                value={filters.product}
                onChange={(e) => handleFilterChange("product", e.target.value)}
              >
                <MenuItem value="">Все продукты</MenuItem>
                <MenuItem value="OSAGO">ОСАГО</MenuItem>
                <MenuItem value="LIFE">Страхование жизни</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth>
              <InputLabel>Модель</InputLabel>
              <Select
                value={filters.model}
                onChange={(e) => handleFilterChange("model", e.target.value)}
              >
                <MenuItem value="">Все модели</MenuItem>
                <MenuItem value="OSAGO">OSAGO</MenuItem>
                <MenuItem value="LIFE">LIFE</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth>
              <InputLabel>Страховой случай</InputLabel>
              <Select
                value={filters.insuranceCase}
                onChange={(e) =>
                  handleFilterChange("insuranceCase", e.target.value)
                }
              >
                <MenuItem value="">Все страховые случаи</MenuItem>
                <MenuItem value="Возник">Возник</MenuItem>
                <MenuItem value="Не возник">Не возник</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth>
              <InputLabel>Фичи</InputLabel>
              <Select
                multiple
                value={filters.features}
                onChange={(e) =>
                  handleFilterChange("features", e.target.value)
                }
              >
                <MenuItem value="feature1">Feature 1</MenuItem>
                <MenuItem value="feature2">Feature 2</MenuItem>
                <MenuItem value="feature3">Feature 3</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <DatePicker
              label="Дата начала"
              value={startDate}
              onChange={(newValue) => setStartDate(newValue)}
              renderInput={(params) => <TextField {...params} fullWidth />}
            />
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <DatePicker
              label="Дата окончания"
              value={endDate}
              onChange={(newValue) => setEndDate(newValue)}
              renderInput={(params) => <TextField {...params} fullWidth />}
            />
          </Grid>
        </Grid>

        <Box mt={3}>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  {columns.map((col) => (
                    <TableCell key={col}>{col}</TableCell>
                  ))}
                </TableRow>
              </TableHead>
              <TableBody>
                {data
                  .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                  .map((row, index) => (
                    <TableRow key={index}>
                      {Object.values(row).map((value, i) => (
                        <TableCell key={i}>{value}</TableCell>
                      ))}
                    </TableRow>
                  ))}
              </TableBody>
            </Table>
          </TableContainer>
          <TablePagination
            component="div"
            count={data.length}
            page={page}
            onPageChange={handlePageChange}
            rowsPerPage={rowsPerPage}
            onRowsPerPageChange={handleRowsPerPageChange}
          />
        </Box>
      </Box>
    </LocalizationProvider>
  );
};

export default DataMart;
