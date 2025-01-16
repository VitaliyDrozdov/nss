import React, { useState } from 'react';
import {
  Typography,
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
  TextField
} from '@mui/material';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import Header from "../../components/Header";

const DataMart = () => {
  const [filters, setFilters] = useState({
    product: '',
    model: '',
    insuranceCase: '',
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

  const columns = [
    'Продукт',
    'ID запроса',
    'ID категории',
    'Дата открытия',
    'Дата закрытия',
    'Модель',
    'Название фичи',
    'Значение фичи',
    'Скор балл',
    'Страховой случай',
  ];

  const rows = [
    // Example rows
    {
      product: 'OSAGO',
      requestId: '123',
      categoryId: '456',
      startDate: '01.12.2024',
      endDate: '31.12.2024',
      model: 'OSAGO',
      featureName: 'driver_region',
      featureValue: 'value',
      score: '0.20',
      insuranceCase: 'Возник',
    },

    {
      product: 'OSAGO',
      requestId: '123',
      categoryId: '456',
      startDate: '01.12.2024',
      endDate: '31.12.2024',
      model: 'OSAGO',
      featureName: 'driver_region',
      featureValue: 'value',
      score: '0.20',
      insuranceCase: 'Возник',
    },

    {
      product: 'OSAGO',
      requestId: '123',
      categoryId: '456',
      startDate: '01.12.2024',
      endDate: '31.12.2024',
      model: 'OSAGO',
      featureName: 'driver_region',
      featureValue: 'value',
      score: '0.20',
      insuranceCase: 'Возник',
    },

    {
      product: 'OSAGO',
      requestId: '123',
      categoryId: '456',
      startDate: '01.12.2024',
      endDate: '31.12.2024',
      model: 'OSAGO',
      featureName: 'driver_region',
      featureValue: 'value',
      score: '0.20',
      insuranceCase: 'Возник',
    },

    {
      product: 'OSAGO',
      requestId: '123',
      categoryId: '456',
      startDate: '01.12.2024',
      endDate: '31.12.2024',
      model: 'OSAGO',
      featureName: 'driver_region',
      featureValue: 'value',
      score: '0.20',
      insuranceCase: 'Возник',
    },

    {
      product: 'OSAGO',
      requestId: '123',
      categoryId: '456',
      startDate: '01.12.2024',
      endDate: '31.12.2024',
      model: 'OSAGO',
      featureName: 'driver_region',
      featureValue: 'value',
      score: '0.20',
      insuranceCase: 'Возник',
    },

    {
      product: 'OSAGO',
      requestId: '123',
      categoryId: '456',
      startDate: '01.12.2024',
      endDate: '31.12.2024',
      model: 'OSAGO',
      featureName: 'driver_region',
      featureValue: 'value',
      score: '0.20',
      insuranceCase: 'Возник',
    },

    {
      product: 'LIFE',
      requestId: '123',
      categoryId: '456',
      startDate: '01.12.2024',
      endDate: '31.12.2024',
      model: 'OSAGO',
      featureName: 'driver_region',
      featureValue: 'value',
      score: '0.20',
      insuranceCase: 'Возник',
    },

    {
      product: 'LIFE',
      requestId: '123',
      categoryId: '456',
      startDate: '01.12.2024',
      endDate: '31.12.2024',
      model: 'OSAGO',
      featureName: 'driver_region',
      featureValue: 'value',
      score: '0.20',
      insuranceCase: 'Возник',
    },

    {
      product: 'OSAGO',
      requestId: '123',
      categoryId: '456',
      startDate: '01.12.2024',
      endDate: '31.12.2024',
      model: 'OSAGO',
      featureName: 'driver_region',
      featureValue: 'value',
      score: '0.20',
      insuranceCase: 'Возник',
    },

    {
      product: 'LIFE',
      requestId: '123',
      categoryId: '456',
      startDate: '01.12.2024',
      endDate: '31.12.2024',
      model: 'OSAGO',
      featureName: 'driver_region',
      featureValue: 'value',
      score: '0.20',
      insuranceCase: 'Возник',
    },
    {
      product: 'OSAGO',
      requestId: '123',
      categoryId: '456',
      startDate: '01.12.2024',
      endDate: '31.12.2024',
      model: 'OSAGO',
      featureName: 'driver_region',
      featureValue: 'value',
      score: '0.20',
      insuranceCase: 'Возник',
    },
  ];

  return (
    <LocalizationProvider dateAdapter={AdapterDateFns}>
        <Header title="Витрина данных"/>
      
      <Box p={3}>
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth>
              <InputLabel>Продукт</InputLabel>
              <Select
                value={filters.product}
                onChange={(e) => handleFilterChange('product', e.target.value)}
              >
                <MenuItem value="OSAGO">ОСАГО</MenuItem>
                <MenuItem value="Страхование жизни">Страхование жизни</MenuItem>
              </Select>
            </FormControl>
          </Grid>

          <Grid item xs={12} sm={6} md={3}>
            <FormControl fullWidth>
              <InputLabel>Модель</InputLabel>
              <Select
                value={filters.model}
                onChange={(e) => handleFilterChange('model', e.target.value)}
              >
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
                onChange={(e) => handleFilterChange('insuranceCase', e.target.value)}
              >
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
                onChange={(e) => handleFilterChange('features', e.target.value)}
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
                {rows
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
            count={rows.length}
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
