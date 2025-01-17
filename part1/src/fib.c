#define N 10000
int main(){
  // Calculate the N first terms of the fibonacci sequence and return
  int fib_array[N];
  fib_array[0]=0;
  fib_array[1]=1;
  for(int i=2;i<N;i++){
    fib_array[i]=fib_array[i-1]+fib_array[i-2];
  }
  return 0;
}
