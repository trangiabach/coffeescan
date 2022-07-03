import { css } from '@emotion/react';
import '@elastic/eui/dist/eui_theme_dark.css'
import 'tailwindcss/tailwind.css'


export const globalStyes = css`
  #__next,
  .guideBody {
    min-height: 100%;
    display: flex;
    flex-direction: column;
    height: 100%;
    margin: 0;
    overflow-x: hidden;
  }

  body::-webkit-scrollbar {
    display: none;
  }

  .search {
    text-align: center;
    margin-left: 21.5vw;
    margin-right: 21.5vw;
    margin-top: 23vh;
  }

  .logoText {
    font-size: 12vh !important;
  }

  .euiFieldSearch:focus {
    background-image: linear-gradient(to top, #d85d48, #d85d48 2px, transparent 2px, transparent 100%);
  }

  .euiSuggestItem__label {
    color: #d85d48;
  }

  .euiSelectableListItem:hover:not([aria-disabled='true']) {
    color: #d85d48;
    background-color: #E89182 !important;
  }

  .euiButton {
    background-color: #d85d48 !important;
    color: #feefdf !important;
  }

  .euiButton:hover {
    background-color: #c3402a !important;
  }

  .euiSuggestItem__description {
    text-align: right;
  }

  .footerText {
    font-size: 3vh !important;
  }

  .footerTextSpan {
    color:  #d85d48;
  }

  .euiIcon--large {
    display: none;
  }

  .euiHeaderLogo__text {
    font-size: 1.5rem !important;
  }

  .header {
    padding-top: 1.5rem;
    padding-bottom: 1.5rem;
  }

  .euiPageSideBar {
    min-width: 60vh;
  }

  .euiPageHeaderContent__titleIcon {
    display: none;
  }

  .euiAccordion {
    padding-top: 1.5rem;
  }

  .navFooter {
    padding-top: 1.5rem;
  }

  .navFooterQuery {
    padding-top: 1rem;
  }

`;
