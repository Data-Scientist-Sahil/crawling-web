import os
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field
from dotenv import load_dotenv
load_dotenv()

class OpenAIModelFee(BaseModel):
    product_name: str = Field(..., description="just the name of the product.")
    ingredients: list[str] = Field(..., description="the full ingredients list of the product name.")

async def main():
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            #url='https://shop.lakmesalon.in/products/dermalogica-biolumin-c-serum',
            url='https://www.paulaschoice.com/ingredient-dictionary?csortb1=ingredientNotRated&csortd1=1&csortb2=ingredientRating&csortd2=1&csortb3=name&csortd3=1&start=0&sz=2000',
            word_count_threshold=1,
            extraction_strategy=LLMExtractionStrategy(
                provider="openai/gpt-4o", api_token=os.getenv('OPENAI_API_KEY'), 
                schema=OpenAIModelFee.schema(),
                extraction_type="schema",
                #wrong instruction please change it accordingly
                # instruction="""From the crawled content, extract all product names along with their full list of ingredients. 
                # Do not miss any products in the entire content. One extracted model JSON format should look like this: 
                # {"product_name": "Lakme Absolute Explore Eye Paint - 3g",
                # "ingredients": ["Cyclopentasiloxane", "Polyethylene", "Trimethylsiloxysilicate", "Calcium Aluminium Borosilicate", "Mica", "Iron Oxides", "Theobroma Cacao(Cocoa) Seed Butter White"]

                # """
                instruction="""
You are an expert in web data extraction and analysis. Your task is to analyze and extract structured information from a webpage that contains information about skincare ingredients.
"""
            ),            
            bypass_cache=True,
        )
        print(result.extracted_content)

if __name__ == "__main__":
    asyncio.run(main())