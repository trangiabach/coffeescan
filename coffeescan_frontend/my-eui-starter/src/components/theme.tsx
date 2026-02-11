import {
  FunctionComponent,
  createContext,
  useContext,
  useState,
  useEffect,
} from 'react';
import { getTheme, enableTheme } from '../lib/theme';

/**
 * React cwnstream components, including `EuiProvider`.
 */
export const GlobalProvider = createContext<{
  colorMode?: string;
  setColorMode?: (colorMode: string) => void;
}>({});

export const Theme: FunctionComponent = ({ children }) => {
  const [colorMode, setColorMode] = useState('light');

  // on initial mount in the browser, use any theme from local storage
  useEffect(() => {
    setColorMode(getTheme());
  }, []);

  // enable the correct theme when colorMode changes
  useEffect(() => enableTheme(colorMode), [colorMode]);

  return (
    <GlobalProvider.Provider value={{ colorMode, setColorMode }}>
      {children}
    </GlobalProvider.Provider>
  );
};

export const useTheme = () => {
  return useContext(GlobalProvider);
};
