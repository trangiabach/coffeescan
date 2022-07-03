import { useRouter } from "next/router"
import Router from "next/router"
import { useState, useEffect, useRef } from "react"
import Head from 'next/head'
import axios from 'axios'
import { 
    EuiProvider,
    EuiSuggest,
    EuiButton,
    EuiHeader,
    EuiHeaderLogo,
    EuiHeaderLinks,
    EuiHeaderLink,
    EuiPage,
    EuiPageSideBar,
    EuiPageHeader,
    EuiPageContent,
    EuiPageBody,
    EuiFlexGrid,
    EuiFlexGroup,
    EuiFlexItem,
    EuiCard,
    EuiBadge,
    EuiSpacer,
    EuiHealth,
    EuiAccordion, 
    EuiPanel, 
    useGeneratedHtmlId,
    EuiText
  } from '@elastic/eui'

  const badges = [
    'default',
    'hollow',
    'primary',
    'success',
    'accent',
    'warning',
    'danger',
];

const SearchResults = () => { 
    const { query } = useRouter()


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

    const PageContent = (props) => {
        const pageQuery = props.query.q
        const SideBar = () => {
            const [searchOptions, setSearchOptions] = useState([])
            const [searchQuery, setSearchQuery] = useState(pageQuery)
            
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
            }

            const SearchButton = () => {
                const goToSearchResult = () => {
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
                onSearch={getInputValue}
                placeholder="Tìm quán cà phê gần đây"
                isVirtualized
                suggestions={searchOptions.map((x) => {
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

        const NavFooter = () => {
            return (
                <div>
                <EuiText className="navFooter">Hiển thị kết quả cho:
                </EuiText>
                 <EuiHealth color="primary" className="navFooterQuery">
                 {pageQuery}
                </EuiHealth>
                </div>
            )
        }

        const PageCards = (props) => {
            const data = useRef([])
            const [ isLoading, setIsLoading ] = useState(null)
            const dataa = []
            useEffect(() => {
                const fetchData = async () => {
                    setIsLoading(true)
                    const response = await axios.post('http://127.0.0.1:8000/api/v1/place-location/', { query: pageQuery})
                    const _data = response.data
                    data.current = _data
                    setIsLoading(false)
                }
                fetchData()
            }, [])
            if (isLoading) {
                return <p>Loading...</p>
            }
            const Accordion = (props) => {
                const simpleAccordionId = useGeneratedHtmlId({ prefix: 'simpleAccordion' });
                if (props.description == "") {
                    return (
                        <EuiAccordion id={simpleAccordionId} buttonContent={props.content}>
                            <EuiPanel color="subdued">
                            Chưa có review
                            </EuiPanel>
                        </EuiAccordion>
                    )
                }
                return (
                    <EuiAccordion id={simpleAccordionId} buttonContent={props.content}>
                        <EuiPanel color="subdued">
                        {props.description}
                        </EuiPanel>
                    </EuiAccordion>
                );
            }
            return (
                <EuiPageContent
                hasBorder={false}
                hasShadow={false}
                paddingSize="none"
            
                borderRadius="none"
                > 
                <Head>
                    <title>Search Results - Coffee Scan ☕</title>
                </Head>
                {data.current.map((x) => {
                    return (                   
                    <EuiCard 
                    title={
                        <EuiFlexGroup>
                            <EuiFlexItem>
                                <a href={"https://www.google.com/search?q=" + x.name + " coffee"}  target="_blank">{x.name}</a>
                            </EuiFlexItem>
                            <EuiSpacer size="m"></EuiSpacer>
                            <EuiFlexItem>
                                <EuiHealth color="success">{x.distance}</EuiHealth>
                            </EuiFlexItem>
                            <EuiFlexItem>
                                <EuiHealth color="warning">{x.duration}</EuiHealth>
                            </EuiFlexItem>
                        </EuiFlexGroup>
                    }
                    description={
                        x.formatted_address}
                    textAlign="left"
                    footer={
                        <div>
                        <EuiFlexGrid gutterSize="m">
                            {x.tags.map((tag) => {
                                return (
                                    <EuiFlexItem>
                                        <EuiBadge color={badges[Math.floor(Math.random() * badges.length)]}>{tag.name}</EuiBadge>
                                    </EuiFlexItem>
                                )
                            })}
                        </EuiFlexGrid>
                        <Accordion content="Xem review cà phê" description={x.coffee_desc}></Accordion>
                        <Accordion content="Xem review không gian" description={x.space_desc}></Accordion>
                    </div>
                    }
                    />
                    )
                })}
                </EuiPageContent>
            )
        }
        return (
            <EuiPage paddingSize="none">
                <EuiPageSideBar paddingSize="l" sticky>
                    <SideBar></SideBar>
                    <NavFooter></NavFooter>
                </EuiPageSideBar>
                <EuiPageBody panelled>
                <EuiPageHeader
                    restrictWidth
                    iconType="logoElastic"
                    pageTitle="☕ Coffee Scan"
                />
                <PageCards></PageCards>
                </EuiPageBody>
            </EuiPage>
        )

    }
    return (
    <EuiProvider colorMode="dark">
        <Header></Header>
        <PageContent query={query}></PageContent>
    </EuiProvider>
    )
}

export default SearchResults