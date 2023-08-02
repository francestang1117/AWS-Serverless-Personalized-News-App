import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import { format } from 'date-fns';
import './news.css'
import 'react-datepicker/dist/react-datepicker.css';
// import { getApiGatewayUrl } from './gateway';

const News = () => {
    // required
    const [email, setEmail] = useState('');
    const [emailSubmitted, setEmailSubmitted] = useState(false);
    const [endpoint, setEndpoint] = useState('');
    // 'everything' parameters
    const [q, setQ] = useState('');
    const [to, setTo] = useState(new Date());
    const [from, setFrom] = useState(new Date());
    const [domains, setDomains] = useState('');
    const [excludeDomains, setExcludeDomains] = useState('');
    const [language, setLanguage] = useState('en');
    const [sortBy, setSortBy] = useState('publishedAt');
    const [searchIn, setSearchIn] = useState({
        title: false,
        description: false,
        content: false
    });

    // 'top-headlines' parameters    
    const [country, setCountry] = useState('');
    const [category, setCategory] = useState('');
    const [pageSize, setPageSize] = useState(20);
    const [page, setPage] = useState(1);
    const [newsData, setNewsData] = useState([]);
    const [error, setError] = useState(null);

    const countryOptions = ['ae', 'ar', 'at', 'au', 'be', 'bg', 'br', 'ca', 'ch', 'cn', 'co', 'cu', 'cz', 'de', 'eg', 'fr', 'gb', 'gr', 'hk', 'hu', 'id', 'ie', 'il', 'in', 'it', 'jp', 'kr', 'lt', 'lv', 'ma', 'mx', 'my', 'ng', 'nl', 'no', 'nz', 'ph', 'pl', 'pt', 'ro', 'rs', 'ru', 'sa', 'se', 'sg', 'si', 'sk', 'th', 'tr', 'tw', 'ua', 'us', 've', 'za'];
    const categoryOptions = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology'];

    // handle email submission
    const handleSubmit = async(e) => {
        e.preventDefault();
        if (!emailSubmitted) {
            setEmailSubmitted(true);
        }else {
            const data = {
                email,
                endpoint,
                parameters: {},
            };

            // add common optional fields if they have been filled
            if (q) data.parameters.q = q;
            if (pageSize) data.parameters.pageSize = pageSize;
            if (page) data.parameters.page = page;

            // add optional fields specific to endpoint 'everything'
            if (endpoint === 'everything') {
                if (Object.keys(searchIn).filter(key => searchIn[key]).length > 0) {
                    data.parameters.searchIn = Object.keys(searchIn).filter(key => searchIn[key]).join(',');
                }
                if (from) data.parameters.from = format(from, 'yyyy-MM-dd');
                if (to) data.parameters.to = format(to, 'yyyy-MM-dd');
                if (language) data.parameters.language = language;
                if (sortBy) data.parameters.sortBy = sortBy;
                if (domains) data.parameters.domains = domains;
                if (excludeDomains) data.parameters.excludeDomains = excludeDomains;
            }

            // add optional fields specific to endpoint 'top-headlines'
            if (endpoint === 'top-headlines') {
                if (country) data.parameters.country = country;
                if (category) data.parameters.category = category;
            }

            // send data to the API Gateway url
            try {
                console.log("start calling");
                const apiUrl = process.env.REACT_APP_APIGATEWAY_URL;
                const response = await fetch(`${apiUrl}/news`, {
                    method: 'POST',
                    body: JSON.stringify(data), 
                });


                if (response.ok) {
                    setError(null);
                    
                    const fetchedData = await response.json();
                    console.log(fetchedData);
                    const fetchedNews = fetchedData.articles_with_sentiments;
                    setNewsData(fetchedNews);
                } else {
                    // Handle HTTP response status code error
                    setNewsData(null);
                    const errorData = await response.json();
                    const errorMessage = errorData.Error;
                    setError(errorMessage);
                }
            } catch (error) {
                console.error('Fetching data failed with error: ', error.message);
                    setError('An error occurred while fetching data. Please try again later.');
            }

        }
    };

    return (
        <div className='container'>
            <form onSubmit={handleSubmit} className='form-container'>
                {!emailSubmitted && (
                    <div>
                        <label>
                            Email:
                            <input type="email" value={email} className='submit-email-butto' onChange={e => setEmail(e.target.value)} required />
                        </label>
                        <input type="submit" value="Submit Email" />
                    </div>
                )}

                {emailSubmitted && (
                    <div>
                        <label>
                            Endpoint:
                            <select value={endpoint} onChange={(e) => setEndpoint(e.target.value)} required>
                                <option value="">--Please choose the endpoint--</option>
                                <option value="everything">everything</option>
                                <option value="top-headlines">top-headlines</option>
                            </select>
                        </label>
                        <label>
                            Query:
                            <input type='text' value={q} onChange={(e) => setQ(e.target.value)} className='param'/>
                        </label>
                        {
                            q && (
                                <label>
                                    Search in: 
                                    <div className='checkbox-container'>
                                        <label>
                                            <input 
                                                type='checkbox' 
                                                name='title' 
                                                checked={searchIn.title}
                                                onChange={(e) => setSearchIn(prevState => ({...prevState, title: e.target.checked}))} 
                                            />
                                            Title
                                        </label>
                                        <label>
                                            <input 
                                                type='checkbox'
                                                checked={searchIn.description}
                                                onChange={(e) => setSearchIn(prevState => ({...prevState, description: e.target.checked}))}
                                            />
                                            Description
                                        </label>
                                        <label>
                                            <input 
                                                type='checkbox'
                                                checked={searchIn.content}
                                                onChange={(e) => setSearchIn(prevState => ({...prevState, content: e.target.checked}))}
                                            />
                                            Content
                                        </label>
                                    </div>
                                </label>
                            )
                        }
                        
                        <label>
                            Page Size (maximum 100):
                            <input type='number' min="1" max="100" value={pageSize} onChange={(e) => setPageSize(e.target.value)} />
                        </label>
                        <label>
                            Page:
                            <input type='number' min="1" value={page} onChange={(e) => setPage(e.target.value)} />
                        </label>
                        {endpoint === 'everything' && (
                            <div>
                                <label>
                                    Language:
                                    <select value={language} onChange={e => setLanguage(e.target.value)} required>
                                        <option value="">--Please select a language--</option>
                                        <option value="ar">Arabic</option>
                                        <option value="de">German</option>
                                        <option value="en">English</option>
                                        <option value="es">Spanish</option>
                                        <option value="fr">French</option>
                                        <option value="he">Hebrew</option>
                                        <option value="it">Italian</option>
                                        <option value="nl">Dutch</option>
                                        <option value="no">Norwegian</option>
                                        <option value="pt">Portuguese</option>
                                        <option value="ru">Russian</option>
                                        <option value="se">Swedish</option>
                                        <option value="ud">Ukrainian</option>
                                        <option value="zh">Chinese</option>
                                    </select>
                                </label>
                                <div>
                                    <label>
                                        From:
                                        <div>
                                            <DatePicker selected={from} onChange={(date) => setFrom(date)} dateFormat="yyyy-MM-dd" />
                                        </div>
                                    </label>
                                </div>
                                <div>
                                    <label>
                                        To:
                                        <div>
                                            <DatePicker selected={to} onChange={(date) => setTo(date)} dateFormat="yyyy-MM-dd" />
                                        </div>
                                    </label>
                                </div>
                                <label>
                                    Sorted By:
                                    <select value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
                                        <option value="">--Please select an option--</option>
                                        <option value="relevancy">Relevancy</option>
                                        <option value="popularity">Popularity</option>
                                        <option value="publishedAt">PublishedAt</option>
                                    </select>
                                </label>
                                <label>
                                    Domains:
                                    <input type='text' value={domains} onChange={(e) => setDomains(e.target.value)} className='param' placeholder='bbc-news,techcrunch' />
                                </label>
                                <label>
                                    ExcludeDomains:
                                    <input type='text' value={excludeDomains} onChange={(e) => setExcludeDomains(e.target.value)} className='param' placeholder='bbc-news,techcrunch' />
                                </label>
                            </div>
                        )}
                        {endpoint === 'top-headlines' && (
                            <div>
                                <label>
                                    Country:
                                        <select value={country} onChange={(e) => setCountry(e.target.value)}>
                                            {countryOptions.map((code) => (
                                                <option key={code} value={code}>
                                                    {code}
                                                </option>
                                            ))}
                                        </select>
                                </label>
                                <label>
                                    Category:
                                        <select value={category} onChange={(e) => setCategory(e.target.value)}>
                                            {categoryOptions.map((option) => (
                                                <option key={option} value={option}>
                                                    {option.charAt(0).toUpperCase() + option.slice(1)}
                                                </option>
                                            ))}
                                        </select>
                                </label>
                            </div>
                        )}
                        <input type="submit" value="Submit" />
                    </div>
                )}
                {error ? (
                    <p className='error'>{error}</p>
                ) : (
                    newsData.length > 0 ? (
                        <div className='result-container'>
                            <h1>Results</h1>
                            {newsData.map((data, index) => (
                                <div key={index} className='data'>
                                    <h2>{data.news.title}</h2>
                                    <h3>Author: {data.news.author}</h3>
                                    <p>Description: {data.news.description}</p>
                                    <p>Published at: {data.news.publish_time}</p>
                                    <p>Sentiment: {data.sentiment}</p>
                                </div>
                            ))}
                        </div>
                    ) : (
                        <p>No news data found.</p>
                    )
                )}

            </form>
        </div>
    );
};

export default News;