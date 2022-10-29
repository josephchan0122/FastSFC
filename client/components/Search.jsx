import React from 'react';
import { throttle, debounce } from 'throttle-debounce';
import { Parser as HTMLParser } from 'html-to-react';

import { hot } from 'react-hot-loader';

/**
 * Autocomplete search component.
 */
class Search extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      /**
       * Current query value
       */
      q: '',
      /**
       * Received from the api result
       */
      companies: [],
      /**
       * Cursor position
       */
      cursor: -1,
    };

    /**
     * Wrapped lookup with throttle
     * @type {wrapper}
     */
    this.autocompleteSearchThrottled = throttle(200, this.autocompleteSearch);

    /**
     * Wrapped lookup with debounce
     * @type {wrapper}
     */

    this.autocompleteSearchDebounced = debounce(200, this.autocompleteSearch);
    /**
     * Instance of the HTML parser (used to fill react components with unescaped HTML)
     * @type {{parse, parseWithInstructions}}
     */
    this.htmlToReactParser = new HTMLParser();
  }

  /**
   * add click listener on mount
   */
  componentWillMount() {
    document.addEventListener('mousedown', this.handleClick, false);
    this.handleKeyDown = this.handleKeyDown.bind(this);
  }

  /**
   * remove click listener on unmount
   */
  componentWillUnmount() {
    document.removeEventListener('mousedown', this.handleClick, false);
  }

  /**
   * Handle selected option with arrows
   * @param e: event
   */
  handleKeyDown(e) {
    const { companies, cursor } = this.state;
    // arrow up/down button should select next/previous list element
    if (e.key === 'ArrowUp' && cursor > -1) {
      e.preventDefault();
      this.setState(prevState => ({
        cursor: prevState.cursor - 1,
      }));
      this.updateStateBasedOnCursor();
    } else if (e.key === 'ArrowDown' && cursor < companies.length - 1) {
      e.preventDefault();
      this.setState(prevState => ({
        cursor: prevState.cursor + 1,
      }));
      this.updateStateBasedOnCursor();
    }
  }

  /**
   * Update query based on the selected list item
   */
  updateStateBasedOnCursor() {
    this.setState(state => {
      const { companies, cursor } = state;
      // add selected ticker
      if (companies[cursor] && companies[cursor].ticker) {
        return { q: companies[cursor].ticker };
      }
      return {};
    });
  }

  /**
   * Handle click events
   * @param e: browser event
   */
  handleClick = e => {
    if (!this.formNode.contains(e.target)) {
      // Clean companies when user clicks outside of the component
      this.setState({ companies: [] });
    }
    if (e.target === this.searchNode) {
      // Trigger change event behaviour when user clicks on search input
      this.handleChangeQuery(e);
    }
  };

  /**
   * Format autocomplete element (company name and ticker)
   * @param company: element received by API
   */
  formatCompany = company => {
    // if ticker is not empty wrap it with <b> tag, else use ''
    const ticker = company.ticker ? `<b>${company.ticker}</b> - ` : '';
    return this.htmlToReactParser.parse(
      // concatenate ticker and company name
      ticker +
        // wrap found elements with <b> tag
        company.short_name.replace(
          new RegExp(this.state.q, 'ig'),
          element => `<b>${element}</b>`
        )
    );
  };

  /**
   * Execute API request if needed
   * @param q: needle for the API search
   */
  autocompleteSearch = q => {
    const url = '/api/v1/company/?limit=5&format=json&search=' + q;
    // check cached value
    const cached = this.autocompleteCache[url];
    // register last needle to the global variable
    this.waitingFor = q;

    if (cached) {
      // do not run query if request is cached
      this.setState({ companies: cached });
    } else {
      fetch(url)
        .then(response => {
          if (response.status === 200 && q === this.waitingFor) {
            // if response is ok and query has latest needle,
            // save result to state and register cache
            response.json().then(r => {
              this.setState({ companies: r.results });
              this.autocompleteCache[url] = r.results;
            });
          }
        })
        .catch();
    }
  };

  /**
   * Handler for the input change
   * @param event
   */
  handleChangeQuery = event => {
    // register query value and run callback and clear cursor
    this.setState({ q: event.target.value, cursor: 0 }, () => {
      if (!this.state.q || !this.state.q.replace(/\s/g, '').length) {
        // do not execute request if query is empty or contains only spaces
        this.setState({ companies: [] });
      } else if (this.state.q.length < 5 || this.state.q.endsWith(' ')) {
        // use throttled handler if query is small
        this.autocompleteSearchThrottled(this.state.q);
      } else {
        // use debounced request if query is longer than 5
        this.autocompleteSearchDebounced(this.state.q);
      }
    });
  };

  /**
   * Handle form submit
   * @param e: event
   */
  handleSubmitForm = e => {
    e.preventDefault();
    const c = this.state.companies[this.state.cursor];
    if (c) {
      window.location = c.ticker ? '/company/' + c.ticker : '/company/' + c.id;
    } else if (this.searchNode.value.length > 0) {
      window.location = '/search?q=' + this.searchNode.value;
    }
  };

  /**
   * Requests cache
   * @type {{}}
   */
  autocompleteCache = {};

  render() {
    const companies = this.state.companies || [];

    return (
      <form
        className="query-form"
        ref={node => {
          this.formNode = node;
        }}
        onSubmit={this.handleSubmitForm}>
        <div className="form-group">
          <input
            placeholder="Search ticker or company..."
            type="text"
            value={this.state.q}
            onKeyDown={this.handleKeyDown}
            onChange={this.handleChangeQuery}
            ref={node => {
              this.searchNode = node;
            }}
            className="mt-input mt-input-search"
            // eslint-disable-next-line react/jsx-closing-bracket-location
          />
          <div className="suggestions">
            {companies.map((c, i) => (
              <a
                key={c.ticker + c.short_name}
                className={
                  this.state.cursor === i
                    ? 'suggestion selectable cursor'
                    : 'suggestion selectable'
                }
                href={c.ticker ? '/company/' + c.ticker : '/company/' + c.id}>
                {this.formatCompany(c)}
              </a>
            ))}
          </div>
        </div>
        <button
          className="btn btn-search btn-search-light btn-typeahead"
          type="submit">
          <i className="fa fa-search" />
        </button>
      </form>
    );
  }
}

export default hot(module)(Search);
