import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

# Yahan apna complete JSON data paste karein
# Maine aapke diye hue data ka structure use kiya hai
STATIC_RESPONSE = {
    "success": True,
    "responseCode": 3001,
    "message": "Courses List",
    "data": [
        {
            "layout_type": "category_list_layout",
            "layout_title": "All Categories",
            "list": []
        },
        {
            "layout_type": "course_list_layout",
            "layout_title": "All Courses",
            "list": [
                {
                    "id": 83,
                    "title": "UP Board ABHAY 10th (हिंदी माध्यम)",
                    "description": "<p>Course description here</p>",
                    "thumbnail": "https://dylnd2lqy6eys.cloudfront.net/540/admin_v1/bundle_management/course/641788840605_Abhay_UP_Board_(1).png",
                    "mrp": "1499.00",
                    "offer_price": "499.00",
                    "cat_type": 0,
                    "shipping_charge": "0.00",
                    "course_type": 1,
                    "tax_rate": 18,
                    "info": {"text": "184: Video, 185: Pdf, 31: test, 20: DPP, 1: Survey"},
                    "duration_type": 3,
                    "days": 0,
                    "start_date": "1763317800",
                    "end_date": "1774981800",
                    "is_featured": "",
                    "is_new": "",
                    "is_trending": "",
                    "average_rating": "0.0",
                    "review_count": 0,
                    "pdf": "",
                    "is_popup": 0,
                    "is_purchased": 0,
                    "valid_from": None,
                    "valid_to": None,
                    "discount_percentage": 66.71
                },
                {
                    "id": 84,
                    "title": "Bihar Board ABHAY 10th(हिंदी माध्यम)",
                    "description": "<p>Bihar Board course description</p>",
                    "thumbnail": "https://dylnd2lqy6eys.cloudfront.net/540/admin_v1/bundle_management/course/777873140606_Abhay_Bihar_Board_(1).png",
                    "mrp": "1499.00",
                    "offer_price": "499.00",
                    "cat_type": 0,
                    "shipping_charge": "0.00",
                    "course_type": 1,
                    "tax_rate": 18,
                    "info": {"text": "190: Video, 188: Pdf, 32: test, 19: DPP, 1: Survey"},
                    "duration_type": 3,
                    "days": 120,
                    "start_date": "1763317800",
                    "end_date": "1774895400",
                    "is_featured": "",
                    "is_new": "",
                    "is_trending": "",
                    "average_rating": "0.0",
                    "review_count": 0,
                    "pdf": "",
                    "is_popup": 0,
                    "is_purchased": 0,
                    "valid_from": None,
                    "valid_to": None,
                    "discount_percentage": 66.71
                }
                # Yahan baaki courses add karein...
            ]
        }
    ]
}

@app.get("/allbatch")
def get_allbatch():
    return JSONResponse(content=STATIC_RESPONSE, status_code=200)

@app.get("/")
def root():
    return {
        "status": "API is running successfully",
        "message": "Static response mode - Hit /allbatch to get course data.",
        "total_courses": len(STATIC_RESPONSE["data"][1]["list"])
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
