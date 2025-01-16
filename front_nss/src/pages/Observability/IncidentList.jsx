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
  Button,
  TextField,
  TableSortLabel,
} from "@mui/material";
import Header from "../../components/Header";

const IncidentTable = () => {
  const [selected, setSelected] = useState([]);
  const [data, setData] = useState([
    {
      id: "123452121341",
      service: "User Management",
      status: "Активен",
      priority: "Высокий",
      description: "",
      date: "15:43 12.12.24",
    },
    {
      id: "123452121342",
      service: "Model monitoring",
      status: "В работе",
      priority: "Средний",
      description: "",
      date: "15:43 12.12.24",
    },
    {
      id: "123452121343",
      service: "User Management",
      status: "Завершен",
      priority: "Низкий",
      description: "",
      date: "15:43 12.12.24",
    },
  ]);

  const handleSelect = (id) => {
    setSelected((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const isSelected = (id) => selected.includes(id);

  return (
    <>
    <Header title="Витрина данных" />
    
    <Box p={3} sx={{ backgroundColor: "#1e1e2f", minHeight: "100vh", color: "#fff" }}>
      <Box display="flex" justifyContent="space-between" mb={2}>
        <Button variant="contained" color="primary">
          Редактировать инцидент
        </Button>
        <Button variant="contained" color="secondary">
          Создать инцидент
        </Button>
      </Box>

      <TableContainer component={Paper} sx={{ backgroundColor: "#2b2b3d" }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>
                <Checkbox />
              </TableCell>
              <TableCell>
                <TextField
                  size="small"
                  variant="outlined"
                  placeholder="ID инцидента"
                  fullWidth
                  sx={{
                    "& .MuiOutlinedInput-root": {
                      color: "#fff",
                      "& fieldset": { borderColor: "#4f4f6f" },
                    },
                  }}
                />
              </TableCell>
              <TableCell>
                <TableSortLabel active={false} direction="asc">
                  Сервис
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel active={false} direction="asc">
                  Состояние инцидента
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel active={false} direction="asc">
                  Приоритет
                </TableSortLabel>
              </TableCell>
              <TableCell>Описание инцидента</TableCell>
              <TableCell>
                <TableSortLabel active={false} direction="asc">
                  Дата изменения
                </TableSortLabel>
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.map((row) => (
              <TableRow key={row.id}>
                <TableCell>
                  <Checkbox
                    checked={isSelected(row.id)}
                    onChange={() => handleSelect(row.id)}
                    sx={{
                      color: "#fff",
                      "&.Mui-checked": { color: "#4caf50" },
                    }}
                  />
                </TableCell>
                <TableCell>{row.id}</TableCell>
                <TableCell>{row.service}</TableCell>
                <TableCell>{row.status}</TableCell>
                <TableCell>{row.priority}</TableCell>
                <TableCell>{row.description}</TableCell>
                <TableCell>{row.date}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
    </>
  );
  
};

export default IncidentTable;