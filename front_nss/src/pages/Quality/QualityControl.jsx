import api from "../../utils/api";
import React, { useState } from "react";
import {
  Box,
  Tabs,
  Tab,
  Typography,
  Switch,
} from "@mui/material";


const QualityControl = () => {
  const [value, setValue] = useState('osago');

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const [groupOsagoSwitches, setGroupOsagoSwitches] = useState({
    0: [false],
    1: [false, false, false],
  });

  const [groupLifeSwitches, setGroupLifeSwitches] = useState({
    0: [false],
    1: [false, false, false],
  });

  const updateDQCheck = async (checkType, productType, condition) => {
    try {
      await api.put(`/dq/manage`, {
        check_type: checkType,
        product_type: productType,
        condition,
      });
    } catch (error) {
      console.error("Ошибка при отправке PATCH запроса:", error);
      throw error;
    }
  };

  const toggleCheck = async (groupIndex, checkIndex, productType, checked) => {
    const checkType = groupIndex === 0 ? "DQ1" : `DQ2.${checkIndex + 1}`;

    try {
      await updateDQCheck(checkType, productType, checked);

      if (productType === 'osago') {
        setGroupOsagoSwitches((prev) => ({
          ...prev,
          [groupIndex]: prev[groupIndex].map((state, idx) =>
            idx === checkIndex ? checked : state
          ),
        }));
      } else {
        setGroupLifeSwitches((prev) => ({
          ...prev,
          [groupIndex]: prev[groupIndex].map((state, idx) =>
            idx === checkIndex ? checked : state
          ),
        }));
      }
    } catch (error) {
      console.error("Ошибка при отправке PUT запроса:", error);
    }
  };

  const groups = [
    {
      title: 'ПРОВЕРКА DQ 1',
      checks: ['Проверка по json-схеме'],
    },
    {
      title: 'ПРОВЕРКИ DQ 2',
      checks: ['проверка 2.1', 'проверка 2.2', 'проверка 2.3'],
    },
  ];

  const SwitchStyle = {
    width: 80,
    height: 40,
    padding: 0,
    marginRight: 10,
    '& .MuiSwitch-switchBase': {
      padding: 0,
      marginTop: 'auto',
      marginBottom: 'auto',
      '&.Mui-checked': {
        transform: 'translateX(40px)',
        color: '#7e6fd3',
      },
    },
    '& .MuiSwitch-thumb': {
      width: 40,
      height: 40,
    },
    '& .MuiSwitch-track': {
      borderRadius: 15,
      backgroundColor: '#acaed1',
    },
    '& .Mui-checked + .MuiSwitch-track': {
      backgroundColor: '#acaed1',
    }
  };

  return (
    <Box sx={{ width: '70%', marginLeft: 'auto', marginRight: 'auto', marginTop: 4 }}>
      <Tabs
        value={value}
        onChange={handleChange}
        textColor="secondary"
        indicatorColor="secondary"
        variant="fullWidth"
        centered
      >
        <Tab value="osago" label="ОСАГО" sx={{ fontSize: "30px" }} />
        <Tab value="life" label="СТРАХОВАНИЕ ЖИЗНИ" sx={{ fontSize: "30px" }} />
      </Tabs>

      <Box sx={{ marginTop: 5, border: '1px solid #fff', borderRadius: "8px" }}>
        {value === 'osago' &&
          groups.map((group, groupIndex) => (
            <Box key={groupIndex}>
              <Box display="flex" justifyContent="space-between" sx={{ marginLeft: 2, marginTop: 5 }}>
                <Typography sx={{ fontSize: "25px", fontWeight: "bold" }}>{group.title}</Typography>
              </Box>

              {group.checks.map((check, checkIndex) => (
                <Box
                  key={checkIndex}
                  display="flex"
                  justifyContent="space-between"
                  sx={{ padding: 3, borderBottom: '1px solid #fff' }}
                >
                  <Typography sx={{ fontSize: "20px" }}>{check}</Typography>
                  <Switch
                    sx={SwitchStyle}
                    checked={groupOsagoSwitches[groupIndex][checkIndex]}
                    onChange={(e) =>
                      toggleCheck(groupIndex, checkIndex, 'osago', e.target.checked)
                    }
                  />
                </Box>
              ))}
            </Box>
          ))}

        {value === 'life' &&
          groups.map((group, groupIndex) => (
            <Box key={groupIndex}>
              <Box display="flex" justifyContent="space-between" sx={{ marginLeft: 2, marginTop: 5 }}>
                <Typography sx={{ fontSize: "25px", fontWeight: "bold" }}>{group.title}</Typography>
              </Box>

              {group.checks.map((check, checkIndex) => (
                <Box
                  key={checkIndex}
                  display="flex"
                  justifyContent="space-between"
                  sx={{ padding: 3, borderBottom: '1px solid #fff' }}
                >
                  <Typography sx={{ fontSize: "20px" }}>{check}</Typography>
                  <Switch
                    sx={SwitchStyle}
                    checked={groupLifeSwitches[groupIndex][checkIndex]}
                    onChange={(e) =>
                      toggleCheck(groupIndex, checkIndex, 'life', e.target.checked)
                    }
                  />
                </Box>
              ))}
            </Box>
          ))}
      </Box>
    </Box>
  );
};

export default QualityControl;