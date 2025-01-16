import React, { useState } from 'react';
import { Tab, Tabs, Box, Switch, Typography } from '@mui/material';

const QualityControl = () => {
  const [value, setValue] = useState('osago');

  const handleChange = (event, newValue) => {
    setValue(newValue);
  };

  const [groupOsagoSwitches, setGroupOsagoSwitches] = useState({
    0: [false, false, false],
    1: [false, false, false],
  });

  const [groupLifeSwitches, setGroupLifeSwitches] = useState({
    0: [false, false, false],
    1: [false, false, false],
  });

  const toggleGroupOsago = (groupIndex, checked) => {
    setGroupOsagoSwitches((prev) => ({
      ...prev,
      [groupIndex]: prev[groupIndex].map(() => checked),
    }));
  };

  const toggleCheckOsago = (groupIndex, checkIndex, checked) => {
    setGroupOsagoSwitches((prev) => ({
      ...prev,
      [groupIndex]: prev[groupIndex].map((state, idx) =>
        idx === checkIndex ? checked : state
      ),
    }));
  };

  const toggleGroupLife = (groupIndex, checked) => {
    setGroupLifeSwitches((prev) => ({
      ...prev,
      [groupIndex]: prev[groupIndex].map(() => checked),
    }));
  };

  const toggleCheckLife = (groupIndex, checkIndex, checked) => {
    setGroupLifeSwitches((prev) => ({
      ...prev,
      [groupIndex]: prev[groupIndex].map((state, idx) =>
        idx === checkIndex ? checked : state
      ),
    }));
  };

  const groups = [
    {
      title: 'ПРОВЕРКИ DQ 1',
      checks: ['проверка 1', 'проверка 2', 'проверка 3'],
    },
    {
      title: 'ПРОВЕРКИ DQ 2',
      checks: ['проверка 1', 'проверка 2', 'проверка 3'],
    },
  ];

  const SwitchStyle = {
    width: 80,
    height: 40,
    padding: 0,
    marginRight: 40,

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
  }

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
                <Switch
                  sx={SwitchStyle}
                  checked={groupOsagoSwitches[groupIndex].every((state) => state)}
                  onChange={(e) => toggleGroupOsago(groupIndex, e.target.checked)}
                />
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
                      toggleCheckOsago(groupIndex, checkIndex, e.target.checked)
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
                <Switch
                  sx={SwitchStyle}
                  checked={groupLifeSwitches[groupIndex].every((state) => state)}
                  onChange={(e) => toggleGroupLife(groupIndex, e.target.checked)}
                />
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
                      toggleCheckLife(groupIndex, checkIndex, e.target.checked)
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