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
    product: "",
    model: "",
    insuranceCase: "",
    features: [],
  });

  const [data, setData] = useState([]);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

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

  const transformData = (apiData) =>
    apiData.map((item) => ({
      "Продукт": item.product_type,
      "ID запроса": item.run_id,
      "ID котировки": item.quote_id,
      "Дата открытия": item.start_date,
      "Дата закрытия": item.end_date,
      "Модель": item.model_name,
      "Название фичи": item.feature_name,
      "Значение фичи": item.feature_value,
      "Скор балл": item.predict,
      "Страховой случай": item.is_insurance_case ? "Возник" : "Не возник",
    }));
  

  const fetchData = async () => {
    try {
      const params = new URLSearchParams();

      if (filters.product) params.append("product", filters.product);
      if (filters.model) params.append("model", filters.model);
      if (filters.insuranceCase) params.append("insurance_case", filters.insuranceCase);
      if (filters.features.length > 0) params.append("features", filters.features.join(","));
      if (startDate) params.append("start_date", startDate.toISOString().split("T")[0]);
      if (endDate) params.append("end_date", endDate.toISOString().split("T")[0]);
      params.append("page", page + 1);
      params.append("per_page", rowsPerPage);
      const response = await api.get(`/dwh/?${params.toString()}`);

      const rows=transformData(response.data.data);
      
      setData(rows);
      console.log(data);
    } catch (error) {
      console.error("Ошибка при загрузке данных:", error);
    }
  };

  useEffect(() => {
    fetchData();
  }, [filters, startDate, endDate, page, rowsPerPage]);

  const columns = [
    "Продукт",
    "ID запроса",
    "ID котировки",
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
                <MenuItem value="true">Возник</MenuItem>
                <MenuItem value="false">Не возник</MenuItem>
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
