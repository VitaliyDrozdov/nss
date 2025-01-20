import React, { useState } from "react";
import {
  Box,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Paper,
  Select,
  MenuItem,
  InputLabel,
  FormControl,
  TableSortLabel,
  IconButton,
  Tabs,
  Tab
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import api from "../../../utils/api";

const AccountManagement = () => {
  const [email, setEmail] = useState("");
  const [role, setRole] = useState("");
  const [search, setSearch] = useState("");
  const [order, setOrder] = useState("asc");
  const [orderBy, setOrderBy] = useState("account");
  const [tab, setTab] = useState(0);
  const [accounts, setAccounts] = useState([
    { account: "Учётная запись 1", date: "Дата создания 1", role: "Администратор" },
    { account: "Учётная запись 2", date: "Дата создания 2", role: "Редактор" },
    { account: "Учётная запись 3", date: "Дата создания 3", role: "Пользователь" },
  ]);

  const getUsers = async () => {
    
      const response = api.get("/auth/admin/users");
      console.log(response.data);
  };

  const password = "test"
  const handleCreateAccount = async () => {
    try {
      const response = await api.post("/auth/register", { email, password });

      if (response.status !== 200) {
        throw new Error("Ошибка регистрации пользователя");
      }

      setAccounts([
        ...accounts,
        { account: email, date: new Date().toLocaleDateString(), role },
      ]);

      setEmail("");
      setRole("");
      
    } catch (error) {
      console.error("Произошла ошибка при регистрации пользователя:", error);
    }
  };


  const handleSort = (property) => {
    const isAscending = orderBy === property && order === "asc";
    setOrder(isAscending ? "desc" : "asc");
    setOrderBy(property);
  };

  const sortedAccounts = [...accounts].sort((a, b) => {
    if (order === "asc") {
      return a[orderBy].localeCompare(b[orderBy]);
    }
    return b[orderBy].localeCompare(a[orderBy]);
  });

  const filteredAccounts = sortedAccounts.filter((account) =>
    account.account.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <Box sx={{ p: 3, backgroundColor: "#2e3440", minHeight: "100vh", color: "#fff" }}>
      <Tabs
        value={tab}
        onChange={(e, newValue) => setTab(newValue)}
        sx={{ mb: 3, backgroundColor: "#4c566a", borderRadius: 1 }}
        TabIndicatorProps={{
          style: { backgroundColor: "#88c0d0" },
        }}
      >
        <Tab label="Управление учётными записями" sx={{ color: "#eceff4" }} />
        <Tab label="Управление ролями и доступом" sx={{ color: "#eceff4" }} />
      </Tabs>

      {tab === 0 && (
        <>
          <Box
            sx={{
              display: "flex",
              flexDirection: "column",
              gap: 2,
              mb: 3,
              p: 2,
              backgroundColor: "#3b4252",
              borderRadius: 1,
            }}
          >
            <h3>Новая учётная запись</h3>
            <TextField
              label="Введите электронную почту пользователя"
              variant="outlined"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              fullWidth
              InputLabelProps={{ style: { color: "#d8dee9" } }}
              InputProps={{
                style: { color: "#eceff4", backgroundColor: "#434c5e" },
              }}
            />
            <FormControl fullWidth>
              <InputLabel style={{ color: "#d8dee9" }}>Выберите роль</InputLabel>
              <Select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                sx={{ backgroundColor: "#434c5e", color: "#eceff4" }}
              >
                <MenuItem value="Администратор">Администратор</MenuItem>
                <MenuItem value="Редактор">Редактор</MenuItem>
                <MenuItem value="Пользователь">Пользователь</MenuItem>
              </Select>
            </FormControl>
            <Button
              variant="contained"
              sx={{
                backgroundColor: "third",
                color: "#eceff4",
              }}
              onClick={handleCreateAccount}
            >
              Создать новую учётную запись
            </Button>
          </Box>

          <Box sx={{ mb: 2, display: "flex", alignItems: "center" }}>
            <TextField
              variant="outlined"
              placeholder="Введите email"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              sx={{
                flex: 1,
                mr: 2,
                input: { color: "#eceff4" },
                backgroundColor: "#434c5e",
              }}
            />
            <IconButton sx={{ color: "#88c0d0" }}>
              <SearchIcon />
            </IconButton>
          </Box>

          <TableContainer component={Paper} sx={{ backgroundColor: "#3b4252" }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell sx={{ color: "#d8dee9" }}>
                    <TableSortLabel
                      active={orderBy === "account"}
                      direction={order}
                      onClick={() => handleSort("account")}
                      sx={{ color: "#d8dee9" }}
                    >
                      Учётная запись
                    </TableSortLabel>
                  </TableCell>
                  <TableCell sx={{ color: "#d8dee9" }}>
                    <TableSortLabel
                      active={orderBy === "date"}
                      direction={order}
                      onClick={() => handleSort("date")}
                      sx={{ color: "#d8dee9" }}
                    >
                      Дата создания
                    </TableSortLabel>
                  </TableCell>
                  <TableCell sx={{ color: "#d8dee9" }}>
                    <TableSortLabel
                      active={orderBy === "role"}
                      direction={order}
                      onClick={() => handleSort("role")}
                      sx={{ color: "#d8dee9" }}
                    >
                      Роль
                    </TableSortLabel>
                  </TableCell>
                  <TableCell sx={{ color: "#d8dee9" }}>Действия</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {filteredAccounts.map((row, index) => (
                  <TableRow key={index}>
                    <TableCell sx={{ color: "#eceff4" }}>{row.account}</TableCell>
                    <TableCell sx={{ color: "#eceff4" }}>{row.date}</TableCell>
                    <TableCell sx={{ color: "#eceff4" }}>{row.role}</TableCell>
                    <TableCell>
                      <Button
                        variant="text"
                        sx={{ color: "#88c0d0", ":hover": { color: "#81a1c1" } }}
                      >
                        Редактировать
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </>
      )}
    </Box>
  );
};

export default AccountManagement;
