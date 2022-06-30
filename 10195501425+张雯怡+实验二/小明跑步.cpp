#include<cstdio>
#include<cstring>
#include<queue>
#include<algorithm>
#define mem(a,p) memset(a,p,sizeof(a))
const int N=1005,M=1e4+10;
int n,m,k,dis[N],fir[N],fi[N],tot=0;
struct point{int ne,to,d;}e[M*2],p[M*2];
struct node{
    int to,d;
    bool operator <(const node&p)const{return p.d<d;}
};
int read(){
    int ans=0,f=1;char c=getchar();
    while(c>='0'&&c<='9'){ans=ans*10+c-48;c=getchar();}
    return ans*f;
}
void ins(int u,int v,int w){
    e[++tot]=(point){fir[u],v,w};fir[u]=tot;
    p[tot]=(point){fi[v],u,w};fi[v]=tot;
}
std::priority_queue<node>q;
int ans[105],sum=0;
void clear(){while(!q.empty())q.pop();}
void dj(){
    dis[1]=0;q.push((node){1,0});
    while(!q.empty()){
        node rt=q.top();q.pop();
        int x=rt.to,w=rt.d;
        if(dis[x]!=w)continue;
        for(int i=fi[x];i;i=p[i].ne){
            int to=p[i].to;
            if(dis[to]>dis[x]+p[i].d)dis[to]=dis[x]+p[i].d,q.push((node){to,dis[to]});
        }
    }
}
void astar(){
    if(dis[n]==dis[0])return;
    q.push((node){n,dis[n]});
    while(!q.empty()){
        node rt=q.top();q.pop();
        if(rt.to==1){
            ans[++sum]=rt.d;
            if(sum==k)return;
        }
        int x=rt.to;rt.d-=dis[x];
        for(int i=fir[x];i;i=e[i].ne){
            int to=e[i].to;
            if(dis[to]==dis[0])continue;
            q.push((node){to,dis[to]+rt.d+e[i].d});
        }
    }
}
int main(){
    n=read();m=read();k=read();
    for(int i=1,a,b,c;i<=m;i++){
        a=read();b=read();c=read();
        ins(a,b,c);
    }
    mem(dis,127);
    dj();clear();
    astar();
    for(int i=1;i<=sum;i++)printf("%d\n",ans[i]);
    for(int i=sum+1;i<=k;i++)printf("-1\n");
    return 0;
}