//事情的起因是这样的，我为了做旅行攻略刷到一款小程序--识途，对这个vip有点想法，尝试破解了半天，可惜没有试用提供数据，只能到此为止，可惜了。。。。。
var body = $response.body;
var url = $request.url;
var obj;

try {
    obj = JSON.parse(body);

    // 处理 "/trace/plan/getPlanListFirst" 请求
    if (url.includes("https://prodapi.10tu.top/trace/plan/getPlanListFirst")) {
        if (obj.data && Array.isArray(obj.data.userVOList)) {
            obj.data.userVOList.forEach(user => {
                user.proExpireTime = "2024-12-18T09:14:49.000+00:00";
                user.proStatus = 2;
                user.rid = "1";
      
            });
            body = JSON.stringify(obj);
        }
    }
    // 处理 "/trace/community/userFollow/getCommunityUser" 请求
    else if (url.includes("https://prodapi.10tu.top/trace/community/userFollow/getCommunityUser")) {
        if (obj.data) {
            obj.data.proExpireTime = "2024-12-18T09:14:49.000+00:00";
            obj.data.proStatus = 2;
            obj.data.rid = "1";
          
            body = JSON.stringify(obj);
        }
    }
    // 处理 "/trace/plan/getPlanDetail" 请求
    else if (url.includes("https://prodapi.10tu.top/trace/plan/getPlanDetail")) {
        if (obj.data && Array.isArray(obj.data.userVOList)) {
            obj.data.userVOList.forEach(user => {
                user.proExpireTime = "2024-12-18T09:14:49.000+00:00";
                user.proStatus = 2;
                user.rid = "1";
             
            });
            body = JSON.stringify(obj);
        }
    }
} catch (e) {
    console.error("Error processing response: ", e);
}

$done({ body });
