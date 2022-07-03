import type { NextPage } from "next"
import Head from 'next/head'
import { useState } from "react"
import axios from 'axios'
import { 
  EuiProvider,
  EuiSuggest,
  EuiFlexGroup,
  EuiFlexItem, 
  EuiSpacer,
  EuiText,
  EuiForm,
  EuiThemeProvider,
  EuiButton,
  EuiHeader,
  EuiHeaderLogo,
  EuiHeaderLinks,
  EuiHeaderLink,
} from '@elastic/eui'
import Router from 'next/router'

const SearchBar = () => {
const [searchOptions, setSearchOptions] = useState([])
const [searchQuery, setSearchQuery] = useState("")

const getInputValue = async (val) => {
  setSearchQuery(val.value)
  try {
    const response = await axios.post('http://127.0.0.1:8000/api/v1/user-location/', { query: val})
    setSearchOptions(response.data)
  } catch (error) {
    console.log(error)
  }
}

const onItemClick = (item) => {
  setSearchQuery(item.label)
  console.log(searchQuery)
}

const SearchButton = () => {
  const goToSearchResult = () => {
    console.log(searchQuery)
    Router.push('/searchresults?q=' + searchQuery)
  }
  return (
    <EuiButton onClick={goToSearchResult}>
      Search
    </EuiButton>
  )
}

return (
    <EuiSuggest
      value={searchQuery}
      aria-label="Suggest"
      onChange={getInputValue}
      placeholder="Tìm quán cà phê hot nhất gần bạn!"
      isVirtualized
      suggestions={searchOptions.map((x) => {
        console.log(x)
        return {
          label: x.formatted_address,
          type: { iconType: 'gisApp', color: 'tint9' },
          description: x.name,
          truncate: false,
        }
      })}
      className="searchBar"
      append={SearchButton()}
      onItemClick={onItemClick}
    />
  )
}

const Logo = () => {
  return (
    <EuiText textAlign="center">
      <h1 className="logoText">Coffee Scan ☕</h1>
    </EuiText>
  )
}

const SearchFooter = () => {
  return (
    <EuiText textAlign="center">
      <h1 className="footerText">Tìm hiểu về <span className="footerTextSpan">hơn 500 quán cà phê</span> hot nhất hiện nay!</h1>
    </EuiText>
  )
}

const Header = () => {
  return (
    <EuiHeader
    className="header"
    theme="dark"
    sections={[
      {
        items: [
          <EuiHeaderLogo href="/">Coffee Scan ☕</EuiHeaderLogo>,
          <EuiHeaderLinks aria-label="App navigation dark theme example">
              <EuiHeaderLink>Log In</EuiHeaderLink>
              <EuiHeaderLink>Sign Up</EuiHeaderLink>
              <EuiHeaderLink iconType="help"> Help</EuiHeaderLink>
          </EuiHeaderLinks>,
        ]
      }
    ]}
    />
  )
}
const Home: NextPage = () => {
  return (
    <EuiProvider colorMode="dark">
      <Head>
        <title>Coffee Scan ☕</title>
      </Head>
      <EuiThemeProvider>
        <Header></Header>
        <EuiForm className="search">
          <EuiFlexGroup alignItems="center">
            <EuiFlexItem>
              <Logo></Logo>
            </EuiFlexItem>
          </EuiFlexGroup>
          <EuiSpacer size="m" />
          <EuiFlexGroup alignItems="center">
            <EuiFlexItem>
              <SearchBar></SearchBar>
            </EuiFlexItem>
          </EuiFlexGroup>
          <EuiSpacer size="xl" />
          <EuiFlexGroup alignItems="center">
            <EuiFlexItem>
              <SearchFooter></SearchFooter>
            </EuiFlexItem>
          </EuiFlexGroup>
        </EuiForm>
      </EuiThemeProvider>
  </EuiProvider>
  )
}

export default Home;
