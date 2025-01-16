import { useState, useEffect } from "react";
import { ProSidebar, Menu, MenuItem, SubMenu } from "react-pro-sidebar";
import { Box, IconButton, Typography, useTheme } from "@mui/material";
import { Link } from "react-router-dom";
import "react-pro-sidebar/dist/css/styles.css";
import { tokens } from "../hooks/useTheme";
import api from "../utils/api";
import { useNavigate } from "react-router-dom";

import StorageOutlinedIcon from '@mui/icons-material/StorageOutlined';
import TimelineOutlinedIcon from "@mui/icons-material/TimelineOutlined";
import MenuOutlinedIcon from "@mui/icons-material/MenuOutlined";
import AssuredWorkloadOutlinedIcon from '@mui/icons-material/AssuredWorkloadOutlined';
import AssignmentTurnedInOutlinedIcon from '@mui/icons-material/AssignmentTurnedInOutlined';
import TuneOutlinedIcon from '@mui/icons-material/TuneOutlined';
import RuleOutlinedIcon from '@mui/icons-material/RuleOutlined';
import AssignmentIndOutlinedIcon from '@mui/icons-material/AssignmentIndOutlined';
import ListAltOutlinedIcon from '@mui/icons-material/ListAltOutlined';
import LegendToggleOutlinedIcon from '@mui/icons-material/LegendToggleOutlined';
import HistoryOutlinedIcon from '@mui/icons-material/HistoryOutlined';
import CalendarMonthOutlinedIcon from '@mui/icons-material/CalendarMonthOutlined';
import RemoveRedEyeOutlinedIcon from '@mui/icons-material/RemoveRedEyeOutlined';
import HealthAndSafetyOutlinedIcon from '@mui/icons-material/HealthAndSafetyOutlined';
import AssessmentOutlinedIcon from '@mui/icons-material/AssessmentOutlined';
import NotificationsNoneOutlinedIcon from '@mui/icons-material/NotificationsNoneOutlined';
import AdminPanelSettingsOutlinedIcon from '@mui/icons-material/AdminPanelSettingsOutlined';
import LockPersonOutlinedIcon from '@mui/icons-material/LockPersonOutlined';
import AddchartOutlinedIcon from '@mui/icons-material/AddchartOutlined';
import GroupsOutlinedIcon from '@mui/icons-material/GroupsOutlined';
import TableChartOutlinedIcon from '@mui/icons-material/TableChartOutlined';

const Item = ({ title, to, icon, selected, setSelected }) => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  return (
    <MenuItem
      active={selected === title}
      style={{
        color: colors.grey[100],
      }}
      onClick={() => setSelected(title)}
      icon={icon}
    >
      <Typography>{title}</Typography>
      <Link to={to} />
    </MenuItem>
  );
};

const CustomTitle = ({ children }) => {
  return (
    <Typography variant="body2" sx={{ whiteSpace: 'nowrap' }}>
      {children}
    </Typography>
  );
};




const Sidebar = () => {
  const theme = useTheme();
  const colors = tokens(theme.palette.mode);
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [selected, setSelected] = useState("/quoteOsago");
  const navigate = useNavigate();
  const [email, setEmail] = useState("");

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const response = await api.get("/auth/profile");
        console.log(response.data);
        setEmail(response.data.email);
      } catch (error) {
        console.error(error);
      }
    };

    fetchProfile();
  },);



  return (
    <Box
      sx={{
        "& .pro-sidebar-inner": {
          background: `${colors.primary[400]} !important`,
        },
        "& .pro-icon-wrapper": {
          backgroundColor: "transparent !important",
        },
        "& .pro-inner-item": {
          padding: "5px 35px 5px 0px !important",
        },
        "& .pro-inner-item:hover": {
          color: "#868dfb !important",
        },
        "& .pro-menu-item.active": {
          color: "#6870fa !important",
        },
      }}
    >
      <ProSidebar collapsed={isCollapsed}
        style={{
          width: isCollapsed ? "60px" : "290px",
          transition: "width 0.3s",
        }}>
        <Menu iconShape="square">
          {/* LOGO AND MENU ICON */}
          <MenuItem
            onClick={() => setIsCollapsed(!isCollapsed)}
            icon={isCollapsed ? <MenuOutlinedIcon /> : undefined}
            style={{
              margin: "10px 0 20px 0",
              color: colors.grey[100],
            }}
          >
            {!isCollapsed && (
              <Box
                display="flex"
                justifyContent="space-between"
                alignItems="center"
                ml="15px"
              >
                <Typography variant="h3" color={colors.grey[100]}>
                  NSS
                </Typography>
                <IconButton onClick={() => setIsCollapsed(!isCollapsed)}>
                  <MenuOutlinedIcon />
                </IconButton>
              </Box>
            )}
          </MenuItem>

          {!isCollapsed && (
            <Box mb="25px">
              <Box display="flex" justifyContent="center" alignItems="center">
                <img
                  alt="profile-user"
                  width="100px"
                  height="100px"
                  src={`../../assets/user.png`}
                  style={{ cursor: "pointer", borderRadius: "50%" }}
                />
              </Box>
              <Box textAlign="center">
                <Typography
                  variant="h2"
                  color={colors.grey[100]}
                  fontWeight="bold"
                  sx={{ m: "10px 0 0 0" }}
                >
                  {email}

                </Typography>
              </Box>
            </Box>
          )}

          <Box paddingLeft={isCollapsed ? undefined : "10%"}>

            <Item
              title="Получить скоринг"
              to="/quoteOsago"
              icon={<AssuredWorkloadOutlinedIcon />}
              selected={selected}
              setSelected={setSelected}
            />

            <SubMenu
              icon={<HealthAndSafetyOutlinedIcon />}
              title="Страхование жизни"
            >
              <Item
                title={
                  <CustomTitle>
                    История котировок
                    <br />
                    пользователя
                  </CustomTitle>
                }
                to="/quoteLifeMyHistory"
                icon={<HistoryOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />

              <Item
                title={
                  <CustomTitle>
                    История всех
                    <br />
                    котировок
                  </CustomTitle>
                }
                to="/quoteLifeAllHistory"
                icon={<CalendarMonthOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />
            </SubMenu>

            <SubMenu
              icon={<AssignmentTurnedInOutlinedIcon />}
              title="Качество данных"
              selected={selected}
              setSelected={setSelected}
            >

              <Item
                title={
                  <CustomTitle>
                    Управление
                    <br />
                    проверками
                  </CustomTitle>
                }
                to="/qualityControl"
                icon={<TuneOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />

              <Item
                title="История проверок"
                to="/qualityHistory"
                icon={<RuleOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />

              <Item
                title={
                  <CustomTitle>
                    История действий
                    <br />
                    администратора
                  </CustomTitle>
                }
                to="/qualityAdminHistory"
                icon={<AssignmentIndOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />

              <Item
                title="Аналитика запросов"
                to="/qualityAnalytics"
                icon={<TimelineOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />
            </SubMenu>

            <SubMenu
              title="Витрина данных"
              icon={<StorageOutlinedIcon />}
              selected={selected}
              setSelected={setSelected}
            >
              <Item
                title="Настройки"
                to="/dataMartSettings"
                icon={<TuneOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />

              <Item
                title="Витрина"
                to="/dataMart"
                icon={<TableChartOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />

            </SubMenu>

            <Item
              title="Каталог моделей"
              to="/modelCatalog"
              icon={<ListAltOutlinedIcon />}
              selected={selected}
              setSelected={setSelected}
            />

            <Item
              title="Мониторинг моделей"
              to="/modelMonitoring"
              icon={<LegendToggleOutlinedIcon />}
              selected={selected}
              setSelected={setSelected}
            />

            <SubMenu
              icon={<RemoveRedEyeOutlinedIcon />}
              title="Наблюдаемость"
            >
              <Item
                title="Дашборд"
                to="/dashboard"
                icon={<AssessmentOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />

              <Item
                title="Список инцидентов"
                to="/incidentList"
                icon={<ListAltOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />

              <Item
                title="Уведомления"
                to="/notifications"
                icon={<NotificationsNoneOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />

            </SubMenu>

            <SubMenu
              icon={<AdminPanelSettingsOutlinedIcon />}
              title="Администрирование"
            >

              <Item
                title={
                  <CustomTitle>
                    Управление
                    <br />
                    учётными записями
                  </CustomTitle>
                }
                to="/manageUsers"
                icon={<TuneOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />
              <Item
                title={
                  <CustomTitle>
                    Управление
                    <br />
                    ролями и доступом
                  </CustomTitle>
                }
                to="/manageRoles"
                icon={<LockPersonOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />
              <Item
                title="Отчётность"
                to="/reporting"
                icon={<AddchartOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />

              <Item
                title={
                  <CustomTitle>
                    Протокол сессий
                    <br />
                    пользователей
                  </CustomTitle>
                }
                to="/userSessionHistory"
                icon={<GroupsOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />

              <Item
                title="Протокол изменений"
                to="/profile"
                icon={<HistoryOutlinedIcon />}
                selected={selected}
                setSelected={setSelected}
              />

            </SubMenu>

          </Box>

        </Menu>
      </ProSidebar>
    </Box>
  );
};

export default Sidebar;
