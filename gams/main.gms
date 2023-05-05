
set
    v_n     north       /N01*N12/
    v_e     east        /E01*E15/
    v_s     south       /S01*S18/
    v_w     west        /W01*W09/
    v       vertices    /#v_n, #v_e, #v_s, #v_w/;
  
alias (v, u);
  
parameter
    K           num of water coolers
    p(v)        normalized popularity vector
    D(v, u)     shortest path distance matrix;

variable
    z           objective;

binary variable
    a(v, u)     assignment matrix
    sol(u)      water cooler placement;

* load distance matrix 
$CALL GDXXRW.EXE D.xlsx par=D rng=A1:BC55
$GDXIN D.gdx
$LOAD D
$GDXIN
display D;

* load popularity vector
$CALL GDXXRW.EXE p.xlsx par=p rdim=1 rng=A1:B54
$GDXIN p.gdx
$LOAD p
$GDXIN
display p;

* init num of water coolers
K = 3;

* define equations
equations
    obj             total popularity-weighted distance
    cap_cons        capacity constraint
    ser_cons(v)     serving constraint
    sol_cons(v, u)  sol constraint;

obj.. z =e= sum((v, u), p(v) * a(v, u) * D(v, u));
sol_cons(v, u).. sol(u) =g= a(v, u);
ser_cons(v).. sum(u, a(v, u)) =g= 1;
cap_cons.. sum(u, sol(u)) =l= K;

* solve the problem
model placement /all/;
solve placement using mip minimizing z;
display z.l, sol.l;
